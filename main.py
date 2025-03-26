from funcoes import buscar_leitores_por_nome, buscar_livros_por_nome, cadastrar_leitor, cadastrar_livro, emprestar_livro, devolver_livro, listar_emprestimos


def menu():
    while True:
        print("\nMenu:")
        print("1. Cadastrar Leitor")
        print("2. Cadastrar Livro")
        print("3. Emprestar ou Devolver Livro")
        print("4. Listar Empréstimos")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Digite o nome do leitor: ")
            endereco = input("Digite o endereço do leitor: ")
            telefone = input("Digite o telefone do leitor: ")
            email = input("Digite o email do leitor: ")
            cadastrar_leitor(nome, endereco, telefone, email)
            print(f"Leitor {nome} cadastrado com sucesso!")

        elif escolha == "2":
            titulo = input("Digite o título do livro: ")
            autor = input("Digite o autor do livro: ")
            quantidade = int(input("Digite a quantidade de exemplares do livro: "))
            cadastrar_livro(titulo, autor, quantidade)
            print(f"Livro {titulo} cadastrado com sucesso!")

        elif escolha == "3":
            # Emprestar ou devolver livro
            acao = input("Você deseja (1) Emprestar ou (2) Devolver um livro? Escolha: ")

            if acao == "1":
                # Emprestar livro
                nome_leitor = input("Digite o nome do leitor: ")
                leitores = buscar_leitores_por_nome(nome_leitor)

                if len(leitores) > 1:
                    print("\nLeitores encontrados:")
                    for i, leitor in enumerate(leitores, 1):
                        print(f"{i}. {leitor[1]} - {leitor[2]}")
                    escolha_leitor = int(input("Escolha o número do leitor: "))
                    id_leitor = leitores[escolha_leitor - 1][0]
                elif len(leitores) == 1:
                    id_leitor = leitores[0][0]
                else:
                    print("Leitor não encontrado.")
                    continue

                nome_livro = input("Digite uma palavra do título do livro: ")
                livros = buscar_livros_por_nome(nome_livro)

                if livros:
                    print("\nLivros encontrados:")
                    for i, livro in enumerate(livros, 1):
                        print(f"{i}. {livro[1]} - {livro[2]}")
                    escolha_livro = int(input("Escolha o número do livro: "))
                    id_livro = livros[escolha_livro - 1][0]

                    emprestar_livro(id_leitor, id_livro)
                    print("Empréstimo realizado com sucesso!")
                else:
                    print("Nenhum livro encontrado com essa palavra no título.")

            elif acao == "2":
                # Devolver livro
                nome_leitor = input("Digite o nome do leitor: ")
                leitores = buscar_leitores_por_nome(nome_leitor)

                if len(leitores) > 1:
                    print("\nLeitores encontrados:")
                    for i, leitor in enumerate(leitores, 1):
                        print(f"{i}. {leitor[1]} - {leitor[2]}")
                    escolha_leitor = int(input("Escolha o número do leitor: "))
                    id_leitor = leitores[escolha_leitor - 1][0]
                elif len(leitores) == 1:
                    id_leitor = leitores[0][0]
                else:
                    print("Leitor não encontrado.")
                    continue

                nome_livro = input("Digite o nome do livro: ")
                livros = buscar_livros_por_nome(nome_livro)

                if len(livros) > 1:
                    print("\nLivros encontrados:")
                    for i, livro in enumerate(livros, 1):
                        print(f"{i}. {livro[1]} - {livro[2]}")
                    escolha_livro = int(input("Escolha o número do livro: "))
                    id_livro = livros[escolha_livro - 1][0]
                elif len(livros) == 1:
                    id_livro = livros[0][0]
                else:
                    print("Livro não encontrado.")
                    continue

                devolver_livro(id_leitor, id_livro)
                print("Devolução realizada com sucesso!")

            else:
                print("Opção inválida. Tente novamente.")

        elif escolha == "4":
            nome_leitor = input("Digite o nome do leitor: ")
            leitores = buscar_leitores_por_nome(nome_leitor)

            if len(leitores) > 1:
                print("\nLeitores encontrados:")
                for i, leitor in enumerate(leitores, 1):
                    print(f"{i}. {leitor[1]} - {leitor[2]}")
                escolha_leitor = int(input("Escolha o número do leitor: "))
                id_leitor = leitores[escolha_leitor - 1][0]
            elif len(leitores) == 1:
                id_leitor = leitores[0][0]
            else:
                print("Leitor não encontrado.")
                continue

            emprestimos = listar_emprestimos(id_leitor)
            if emprestimos:
                print("\nEmpréstimos do Leitor:")
                for emprestimo in emprestimos:
                    print(f"Livro: {emprestimo[0]} | Empréstimo: {emprestimo[1]} | Devolução: {emprestimo[2]}")
            else:
                print("Este leitor não possui empréstimos.")

        elif escolha == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
