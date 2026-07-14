import sys
sys.path.insert(0, 'c:\\projetos\\grandprix')

try:
    from backend.app import app
    print("✅ backend.app importado com sucesso")
    
    from backend.models import db, Usuario, Produto, OrdemProducao, TarefaKanban, Kpi, Cronograma
    print("✅ Todos os modelos importados com sucesso")
    
    from backend.config import Config
    print("✅ Config importada com sucesso")
    
    print("\n=== Verificações das rotas ===")
    rules = []
    for rule in app.url_map.iter_rules():
        rules.append(f"  {rule.rule} -> {rule.endpoint}")
    rules.sort()
    for r in rules:
        print(r)
    
    print(f"\nTotal de rotas registradas: {len(rules)}")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()