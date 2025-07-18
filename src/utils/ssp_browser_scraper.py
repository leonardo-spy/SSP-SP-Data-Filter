#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitário de Scraping com Browser usando Pydoll
Acessa o site da SSP-SP e extrai links de download
"""

import asyncio
import os
import time
import requests
from typing import Dict, Optional, Union
from bs4 import BeautifulSoup
import ast
try:
    from ..config.settings import settings
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings

def extract_value(result):
    """Extrai o valor real de uma resposta do Pydoll"""
    if isinstance(result, dict) and 'result' in result:
        if 'value' in result['result']:
            return result['result']['value']
        else:
            return result['result']
    return result

def extract_html_puro_from_file(filepath: str) -> str:
    """Lê um arquivo HTML salvo (puro ou wrapper) e retorna o HTML puro"""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    try:
        data = ast.literal_eval(raw)
        # Tenta extrair o campo correto
        if isinstance(data, dict):
            if 'result' in data and 'value' in data['result']:
                return data['result']['value']
            elif 'result' in data and 'result' in data['result'] and 'value' in data['result']['result']:
                return data['result']['result']['value']
    except Exception:
        pass
    return raw

def extract_links_from_html(html: str) -> Dict[str, Dict[int, str]]:
    """Extrai links de download do HTML usando BeautifulSoup"""
    soup = BeautifulSoup(html, 'lxml')
    links = {}
    categorias = {
        "dados_criminais": "Dados criminais",
        "dados_produtividade": "Dados de Produtividade",
        "morte_intervencao": "Morte Decorrente de Intervenção Policial",
        "celulares_subtraidos": "Celulares subtraídos",
        "veiculos_subtraidos": "Veículos subtraídos",
        "objetos_subtraidos": "Objetos subtraídos"
    }
    
    for key, label in categorias.items():
        links[key] = {}
        
        for li in soup.find_all('li'):
            b = li.find('b')
            if b and b.get_text(strip=True).lower() == label.lower():
                ul = li.find('ul')
                if not ul:
                    continue
                
                for a in ul.find_all('a', href=True):
                    li_ano = a.find('li')
                    if li_ano:
                        text = li_ano.get_text(strip=True)
                        if text.isdigit():
                            ano = int(text)
                            href = a['href']
                            links[key][ano] = href
                    else:
                        text = a.get_text(strip=True)
                        if text.isdigit():
                            ano = int(text)
                            href = a['href']
                            links[key][ano] = href
    
    return links

class SSPBrowserScraper:
    """Scraper usando Pydoll para acessar o site da SSP-SP"""
    def __init__(self, url: Optional[str] = None, headless: Optional[bool] = None):
        self.url = url or settings.CONSULTAS_URL
        # Centralizar configuração: parâmetro > settings > env var
        if headless is not None:
            self.headless = headless
        else:
            self.headless = settings.PYDOLL_HEADLESS
    def get_links(self) -> Dict[str, Dict[int, str]]:
        try:
            return asyncio.run(self._get_links_async())
        except Exception as e:
            print(f"Erro ao extrair links: {e}")
            return {}
    async def _get_links_async(self) -> Dict[str, Dict[int, str]]:
        from pydoll.browser import Chrome  # Import local para evitar erro de linter
        # Tentar primeiro com o modo headless configurado
        for headless_try in [self.headless, False]:
            async with Chrome() as browser:
                tab = await browser.start(headless=headless_try)
                try:
                    await tab.go_to(self.url)
                    # Espera ativa até que o DOM tenha pelo menos um <a> de download (.xlsx) ou timeout
                    max_wait = 30  # segundos
                    interval = 1   # segundos
                    elapsed = 0
                    timeout_html_path = os.path.join(settings.DOWNLOADS_DIR, f'ssp_consultas_timeout_{'headless' if headless_try else 'gui'}.html')
                    found = False
                    while elapsed < max_wait:
                        # Esperar por <a> de download
                        a_count_result = await tab.execute_script("document.querySelectorAll('a[href$=.xlsx]').length")
                        a_count = extract_value(a_count_result)
                        if isinstance(a_count, dict):
                            a_count = 0
                        else:
                            a_count = int(a_count) if a_count else 0
                        if settings.DEBUG:
                            print(f"[DEBUG] {elapsed}s: <a> .xlsx encontrados: {a_count}")
                        if a_count > 0:
                            found = True
                            if settings.DEBUG:
                                print(f"[DEBUG] DOM pronto após {elapsed}s (<a> .xlsx={a_count})")
                            break
                        # Também tentar por texto de categoria
                        text_check = await tab.execute_script("document.body.innerText.includes('Dados criminais')")
                        text_found = extract_value(text_check)
                        if text_found:
                            found = True
                            if settings.DEBUG:
                                print(f"[DEBUG] DOM pronto após {elapsed}s (texto 'Dados criminais' encontrado)")
                            break
                        await asyncio.sleep(interval)
                        elapsed += interval
                    if not found and settings.DEBUG:
                        print(f"[DEBUG] Timeout: Nenhum <a> .xlsx ou texto de categoria encontrado após {max_wait}s")
                        # Salvar HTML imediatamente para depuração
                        html_content = await tab.execute_script("document.documentElement.outerHTML")
                        if isinstance(html_content, dict):
                            html_content = extract_value(html_content)
                        if not isinstance(html_content, str):
                            html_content = str(html_content)
                        with open(timeout_html_path, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        print(f"[DEBUG] HTML salvo no timeout em: {timeout_html_path}")
                        # Tentar extrair links do HTML mesmo assim
                        links = extract_links_from_html(html_content)
                        if links and any(links.values()):
                            print(f"[DEBUG] Links extraídos do HTML salvo no timeout!")
                            return links
                    # Salvar HTML renderizado para debug (após espera)
                    html_content = await tab.execute_script("document.documentElement.outerHTML")
                    if settings.DEBUG:
                        print(f"[DEBUG] Tipo do html_content: {type(html_content)}")
                        print(f"[DEBUG] Valor bruto do html_content: {repr(html_content)[:200]} ...")
                    if isinstance(html_content, dict):
                        html_content = extract_value(html_content)
                    if not isinstance(html_content, str):
                        html_content = str(html_content)
                    html_path = os.path.join(settings.DOWNLOADS_DIR, f'ssp_consultas_rendered_{'headless' if headless_try else 'gui'}.html')
                    if settings.DEBUG:
                        with open(html_path, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        print(f"[DEBUG] HTML renderizado salvo em: {html_path}")
                    # Tentar extrair links normalmente
                    links = extract_links_from_html(html_content)
                    if links and any(links.values()):
                        return links
                    else:
                        if settings.DEBUG:
                            print(f"[DEBUG] Nenhum link encontrado com headless={headless_try}. Tentando modo alternativo...")
                finally:
                    await browser.stop()
        return {}  # Se não encontrar links em nenhum modo
    def download_file(self, url: str, filename: str) -> bool:
        try:
            # Corrigir URL relativa para absoluta
            if url.startswith('assets/') or url.startswith('/'):
                from urllib.parse import urljoin
                base_url = 'https://www.ssp.sp.gov.br/'
                url = urljoin(base_url, url)
            file_path = os.path.join(settings.DOWNLOADS_DIR, filename)
            response = requests.get(url, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Arquivo baixado: {filename}")
            return True
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")
            return False
    def _map_category_name_to_key(self, category_name: str) -> Optional[str]:
        category_mapping = {
            "Dados criminais": "dados_criminais",
            "Dados de Produtividade": "dados_produtividade",
            "Morte Decorrente de Intervenção Policial": "morte_intervencao",
            "Celulares subtraídos": "celulares_subtraidos",
            "Veículos subtraídos": "veiculos_subtraidos",
            "Objetos subtraídos": "objetos_subtraidos"
        }
        return category_mapping.get(category_name)
    def _extract_year_from_text(self, text: str) -> Optional[int]:
        import re
        year_match = re.search(r'\b(20\d{2})\b', text)
        if year_match:
            return int(year_match.group(1))
        return None
    @staticmethod
    def analyze_local_html(filepath: str) -> Dict[str, Dict[int, str]]:
        """Analisa um arquivo HTML salvo localmente (puro ou wrapper) e retorna os links extraídos"""
        html = extract_html_puro_from_file(filepath)
        return extract_links_from_html(html) 