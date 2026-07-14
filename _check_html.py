import os
import re
import glob

base = 'c:/projetos/grandprix'

print("=" * 60)
print("VERIFICANDO REFERÊNCIAS A api.js EM TODOS OS HTMLs")
print("=" * 60)

html_files = sorted(glob.glob(os.path.join(base, '*.html')))

for f in html_files:
    name = os.path.basename(f)
    content = open(f, 'r', encoding='utf-8').read()
    # Find api.js references
    refs = re.findall(r'src=\"([^\"]*api\.js[^\"]*)\"', content, re.IGNORECASE)
    print(f"\n📄 {name}:")
    if refs:
        for r in refs:
            print(f"   ✅ api.js ref: {r}")
            # Check if file exists at that path
            full_path = os.path.normpath(os.path.join(base, r))
            if os.path.exists(full_path):
                print(f"      -> OK: arquivo encontrado em {full_path}")
            else:
                print(f"      ❌ PROBLEMA: arquivo NÃO encontrado em {full_path}")
    else:
        # Check if it has inline script instead
        has_api_request = re.search(r'apiRequest\(|carregarDashboard\(|listarProdutos\(|listarOrdens\(|listarUsuarios\(|listarTarefas\(|listarKpis\(|listarCronogramas\(', content)
        if has_api_request:
            print(f"   ❌ Usa funções da API mas NÃO tem referência à api.js!")

print("\n" + "=" * 60)
print("VERIFICANDO ERROS COMUNS NOS HTMLs")
print("=" * 60)

for f in html_files:
    name = os.path.basename(f)
    content = open(f, 'r', encoding='utf-8').read()
    errors = []
    
    # Check for broken HTML
    if '</script' in content and '<script' in content:
        open_scripts = len(re.findall(r'<script[^>]*>', content))
        close_scripts = len(re.findall(r'</script>', content))
        if open_scripts != close_scripts:
            errors.append(f"❌ Script tags desbalanceadas: {open_scripts} abertos, {close_scripts} fechados")
    
    if errors:
        print(f"\n📄 {name}:")
        for e in errors:
            print(f"   {e}")

print("\n✅ Verificação concluída!")