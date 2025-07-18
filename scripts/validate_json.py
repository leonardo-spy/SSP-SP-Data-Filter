#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para validar arquivos JSON na pasta output
"""

import os
import json
import sys

def validate_json_files(output_dir="output"):
    """Valida todos os arquivos JSON no diretório"""
    print(f"Validando arquivos JSON em: {output_dir}")
    print("=" * 50)
    
    if not os.path.exists(output_dir):
        print(f"❌ Diretório {output_dir} não encontrado")
        return
    
    json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
    
    if not json_files:
        print("❌ Nenhum arquivo JSON encontrado")
        return
    
    corrupted_files = []
    valid_files = []
    
    for filename in sorted(json_files):
        file_path = os.path.join(output_dir, filename)
        file_size = os.path.getsize(file_path)
        
        print(f"\n📄 Validando: {filename} ({file_size:,} bytes)")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar se tem a estrutura esperada
            if isinstance(data, dict) and 'dados' in data:
                registros = len(data.get('dados', []))
                print(f"   ✅ Válido - {registros} registros")
                valid_files.append(filename)
            else:
                print(f"   ⚠️  Estrutura inesperada")
                corrupted_files.append(filename)
                
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON inválido: {e}")
            corrupted_files.append(filename)
        except Exception as e:
            print(f"   ❌ Erro ao ler arquivo: {e}")
            corrupted_files.append(filename)
    
    print("\n" + "=" * 50)
    print(f"📊 Resumo:")
    print(f"   ✅ Arquivos válidos: {len(valid_files)}")
    print(f"   ❌ Arquivos corrompidos: {len(corrupted_files)}")
    
    if corrupted_files:
        print(f"\n❌ Arquivos corrompidos:")
        for filename in corrupted_files:
            print(f"   - {filename}")
        
        # Perguntar se deve remover arquivos corrompidos
        response = input(f"\nDeseja remover os {len(corrupted_files)} arquivos corrompidos? (s/N): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            for filename in corrupted_files:
                file_path = os.path.join(output_dir, filename)
                try:
                    os.remove(file_path)
                    print(f"   🗑️  Removido: {filename}")
                except Exception as e:
                    print(f"   ❌ Erro ao remover {filename}: {e}")
    
    return len(corrupted_files) == 0

if __name__ == "__main__":
    success = validate_json_files()
    sys.exit(0 if success else 1) 