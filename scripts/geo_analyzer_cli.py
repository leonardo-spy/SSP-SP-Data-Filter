#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador Geográfico CLI
Uso: python scripts/geo_analyzer_cli.py "query" --raio 5 --export --output-file arquivo.json
"""

import sys
import os
import argparse

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Analisador Geográfico SSP-SP')
    parser.add_argument('query', help='Rua ou coordenadas (formato: "lat,lon")')
    parser.add_argument('--raio', type=float, default=5.0, help='Raio em km (padrão: 5)')
    parser.add_argument('--output-dir', default='output', help='Diretório com arquivos JSON')
    parser.add_argument('--export', action='store_true', help='Exportar resultados detalhados para JSON')
    parser.add_argument('--output-file', help='Nome do arquivo de saída para exportação')
    
    args = parser.parse_args()
    
    try:
        # Importar módulos dinamicamente
        from analyzers.geo_analyzer import GeoAnalyzer
        
        # Criar analisador
        analyzer = GeoAnalyzer(args.output_dir)
        
        # Realizar busca
        records = analyzer.search_and_analyze(args.query, args.raio)
        
        # Imprimir resultados
        analyzer.print_results(records, args.query, args.raio)
        
        # Exportar se solicitado
        if args.export:
            output_file = analyzer.export_detailed_results(
                records, args.query, args.raio, args.output_file
            )
            if output_file:
                print(f"\n💾 Resultados exportados para: {output_file}")
            else:
                print("\n❌ Erro ao exportar resultados")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 