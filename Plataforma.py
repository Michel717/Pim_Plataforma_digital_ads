import json
import os
import hashlib
import statistics
import re

ARQUIVO_USUARIOS = "usuarios.json"

# ───────────── SEGURANÇA ─────────────

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def senha_forte(senha):
    if len(senha) < 8:
        return False
    if not re.search(r"[A-Z]", senha):
        return False
    if not re.search(r"[a-z]", senha):
        return False
    if not re.search(r"[0-9]", senha):
        return False
    if not re.search(r"[\W_]", senha):  # símbolos
        return False
    return True

def ocultar_email(email):
    if "@" not in email:
        return "email inválido"
    
    parte = email.split("@")
    if len(parte[0]) > 3:
        nome_oculto = parte[0][:3] + "***"
    else:
        nome_oculto = parte[0] + "***"
    return f"{nome_oculto}@{parte[1]}"

# ───────────── ARQUIVOS JSON ─────────────

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        try:
            with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

# ───────────── FUNÇÕES DO SISTEMA ─────────────

def cadastrar_usuario():
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    email = input("Email: ")

    # Consentimento do titular
    consentimento = input("Você autoriza o uso dos seus dados para fins educacionais? (s/n): ").strip().lower()
    if consentimento != 's':
        print("❌ Cadastro cancelado por falta de consentimento.")
        return

    print("Escolha o curso:")
    print("1. Lógica Computacional")
    print("2. Segurança Digital")
    print("3. Programação em Python")
    while True:
        opcao_curso = input("Digite 1, 2 ou 3: ")
        if opcao_curso == "1":
            curso = "Lógica Computacional"
            break
        elif opcao_curso == "2":
            curso = "Segurança Digital"
            break
        elif opcao_curso == "3":
            curso = "Programação em Python"
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

    while True:
        senha = input("Senha (mínimo 8 caracteres, com maiúsculas, minúsculas, número e símbolo): ")
        if senha_forte(senha):
            break
        else:
            print("❌ Senha fraca. Tente novamente.")

    senha_hash = criptografar_senha(senha)

    usuario = {
        "nome": nome,
        "idade": idade,
        "email": email,
        "senha": senha_hash,
        "curso": curso
    }

    usuarios = carregar_usuarios()
    usuarios.append(usuario)
    salvar_usuarios(usuarios)
    print("✅ Usuário cadastrado com sucesso!")

def fazer_login():
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = criptografar_senha(senha)

    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha_hash:
            print(f"✅ Login bem-sucedido!")
            print(f"👋 Bem-vindo(a), {usuario['nome']}!")
            print(f"🎓 Curso: {usuario.get('curso', 'Não informado')}")
            return
    print("❌ E-mail ou senha incorretos.")

def excluir_usuario():
    print("🔐 Para excluir sua conta, informe seus dados:")
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = criptografar_senha(senha)

    usuarios = carregar_usuarios()
    novos_usuarios = [u for u in usuarios if not (u["email"] == email and u["senha"] == senha_hash)]

    if len(novos_usuarios) != len(usuarios):
        salvar_usuarios(novos_usuarios)
        print("🗑️ Conta excluída com sucesso.")
    else:
        print("❌ E-mail ou senha incorretos. Nenhum dado foi removido.")

def listar_usuarios():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("⚠ Nenhum usuário cadastrado.")
        return
    for i, u in enumerate(usuarios, start=1):
        email_oculto = ocultar_email(u["email"])
        print(f"{i}. Nome: {u['nome']}, Idade: {u['idade']}, Curso: {u.get('curso', '-')}, Email: {email_oculto}")

def mostrar_estatisticas():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("⚠ Nenhum usuário cadastrado para gerar estatísticas.")
        return

    idades = [u["idade"] for u in usuarios]

    media = statistics.mean(idades)
    mediana = statistics.median(idades)
    try:
        moda = statistics.mode(idades)
    except statistics.StatisticsError:
        moda = "Não há moda (valores únicos ou múltiplos igualmente frequentes)"

    print("\n📊 Estatísticas de Idade dos Usuários:")
    print(f"Média: {media:.2f}")
    print(f"Mediana: {mediana}")
    print(f"Moda: {moda}")

def gerar_relatorio():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("⚠ Nenhum usuário para gerar relatório.")
        return

    idades = [u["idade"] for u in usuarios]
    
    media = statistics.mean(idades)
    mediana = statistics.median(idades)
    try:
        moda = statistics.mode(idades)
    except statistics.StatisticsError:
        moda = "Não há moda"

    with open("relatorio.txt", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE USUÁRIOS\n")
        f.write("======================\n\n")

        for i, u in enumerate(usuarios, start=1):
            email_oculto = ocultar_email(u["email"])
            f.write(f"{i}. Nome: {u['nome']}, Idade: {u['idade']}, Curso: {u.get('curso', '-')}, Email: {email_oculto}\n")

        f.write("\nESTATÍSTICAS DE IDADE\n")
        f.write("----------------------\n")
        f.write(f"Média: {media:.2f}\n")
        f.write(f"Mediana: {mediana}\n")
        f.write(f"Moda: {moda}\n")

    print("📄 Relatório gerado com sucesso: relatorio.txt")

# ───────────── MENU ─────────────

def menu():
    while True:
        print("\n🧠 Plataforma de Educação Digital Segura")
        print("1. Login")
        print("2. Cadastrar usuário")
        print("3. Listar usuários")
        print("4. Ver estatísticas de idade")
        print("5. Gerar relatório em .txt")
        print("6. Excluir minha conta")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            fazer_login()
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "4":
            mostrar_estatisticas()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "6":
            excluir_usuario()
        elif opcao == "7":
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

# ───────────── EXECUÇÃO ─────────────

menu()
