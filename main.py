"""
main.py
Sistema interativo de Gestão de Projetos e Tarefas (POO) - CRUD completo.
Autores: Alexsandra & Luciana
"""

from datetime import datetime, date
from typing import List, Optional


# -----------------------
# Classes de domínio
# -----------------------
class Gestor:
    def __init__(self, nome: str):
        self.nome = nome
        self.projetos: List[Projeto] = []

    def adicionar_projeto(self, projeto: "Projeto"):
        self.projetos.append(projeto)
        projeto.gestor = self

    def remover_projeto(self, projeto: "Projeto"):
        self.projetos.remove(projeto)
        projeto.gestor = None

    def listar_projetos(self):
        if not self.projetos:
            print("  (nenhum projeto cadastrado)")
            return
        for i, p in enumerate(self.projetos, start=1):
            print(f"  {i}. {p.nome} (tarefas: {len(p.tarefas)})")

    def listar_todas_tarefas(self):
        if not self.projetos:
            print("  (nenhum projeto cadastrado)")
            return
        for p in self.projetos:
            print(f"\nProjeto: {p.nome}")
            p.listar_tarefas()


class Projeto:
    def __init__(self, nome: str):
        self.nome = nome
        self.tarefas: List[Tarefa] = []
        self.gestor: Optional[Gestor] = None

    def adicionar_tarefa(self, tarefa: "Tarefa"):
        self.tarefas.append(tarefa)
        tarefa.projeto = self

    def remover_tarefa(self, tarefa: "Tarefa"):
        self.tarefas.remove(tarefa)
        tarefa.projeto = None

    def listar_tarefas(self):
        if not self.tarefas:
            print("  (nenhuma tarefa cadastrada)")
            return
        for i, t in enumerate(self.tarefas, start=1):
            prazo_str = t.prazo.strftime("%d/%m/%Y") if t.prazo else "Sem prazo"
            print(f"  {i}. {t.nome} | Status: {t.status} | Prioridade: {t.prioridade} | Prazo: {prazo_str}")


class Tarefa:
    def __init__(self, nome: str, descricao: str, prioridade: str = "Média", prazo: Optional[date] = None):
        self.nome = nome
        self.descricao = descricao
        self.status = "Pendente"  # Pendente / Em andamento / Concluída
        self.projeto: Optional[Projeto] = None
        self.prioridade = prioridade  # Baixa / Média / Alta
        self.prazo = prazo

    def atualizar_status(self, novo_status: str):
        self.status = novo_status

    def atualizar_dados(self, nome: Optional[str] = None, descricao: Optional[str] = None,
                       prioridade: Optional[str] = None, prazo: Optional[Optional[date]] = None):
        if nome:
            self.nome = nome
        if descricao:
            self.descricao = descricao
        if prioridade:
            self.prioridade = prioridade
        # prazo pode ser None explícito para "sem prazo"
        if prazo is not None:
            self.prazo = prazo


# -----------------------
# Helpers / Utilidades
# -----------------------
def parse_date(datestr: str) -> Optional[date]:
    """Converte 'dd/mm/aaaa' para date; retorna None se vazio ou inválido."""
    if not datestr.strip():
        return None
    try:
        return datetime.strptime(datestr.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def input_int(prompt: str, minimo: int = None, maximo: int = None) -> int:
    """Pede um inteiro e valida limites se fornecidos."""
    while True:
        val = input(prompt).strip()
        if not val:
            print("Entrada vazia. Digite um número.")
            continue
        if not val.isdigit():
            print("Digite um número válido.")
            continue
        n = int(val)
        if minimo is not None and n < minimo:
            print(f"Valor mínimo: {minimo}")
            continue
        if maximo is not None and n > maximo:
            print(f"Valor máximo: {maximo}")
            continue
        return n


def escolher_item(lista: List, titulo: str):
    """Mostra lista enumerada e retorna o item escolhido (ou None)."""
    if not lista:
        print(f"{titulo}: (lista vazia)")
        return None
    for i, item in enumerate(lista, start=1):
        # tenta mostrar atributo nome
        name = getattr(item, "nome", str(item))
        print(f"  {i}. {name}")
    escolha = input_int(f"Escolha o número do {titulo} (ou 0 para cancelar): ", minimo=0, maximo=len(lista))
    if escolha == 0:
        return None
    return lista[escolha - 1]


# -----------------------
# Menu interativo
# -----------------------
def menu():
    print("\n=== SISTEMA DE PROJETOS E TAREFAS ===")
    print("1. Criar Gestor")
    print("2. Criar Projeto")
    print("3. Criar Tarefa")
    print("4. Listar Projetos de um Gestor")
    print("5. Listar Tarefas de um Projeto")
    print("6. Atualizar Status de uma Tarefa")
    print("7. Editar dados de uma Tarefa (nome/descrição/prioridade/prazo)")
    print("8. Listar Todas as Tarefas de um Gestor")
    print("9. Excluir Projeto")
    print("10. Excluir Tarefa")
    print("0. Sair")


def main_loop():
    gestores: List[Gestor] = []

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do Gestor: ").strip()
            if nome:
                gestores.append(Gestor(nome))
                print("Gestor criado com sucesso!")
            else:
                print("Nome vazio. Cancelado.")

        elif opcao == "2":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                nome = input("Nome do Projeto: ").strip()
                if nome:
                    projeto = Projeto(nome)
                    gestor.adicionar_projeto(projeto)
                    print("Projeto adicionado ao gestor!")
                else:
                    print("Nome vazio. Cancelado.")

        elif opcao == "3":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                projeto = escolher_item(gestor.projetos, "projeto")
                if projeto:
                    nome = input("Nome da Tarefa: ").strip()
                    descricao = input("Descrição da Tarefa: ").strip()
                    prioridade = input("Prioridade (Baixa/Média/Alta) [Média]: ").strip() or "Média"
                    prazo_str = input("Prazo (dd/mm/aaaa) ou Enter para sem prazo: ").strip()
                    prazo = parse_date(prazo_str)
                    if prazo_str and prazo is None:
                        print("Formato de data inválido. Use dd/mm/aaaa. Tarefa cancelada.")
                    elif nome:
                        tarefa = Tarefa(nome, descricao, prioridade, prazo)
                        projeto.adicionar_tarefa(tarefa)
                        print("Tarefa criada com sucesso!")
                    else:
                        print("Nome vazio. Cancelado.")

        elif opcao == "4":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                print(f"\nProjetos de {gestor.nome}:")
                gestor.listar_projetos()

        elif opcao == "5":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                projeto = escolher_item(gestor.projetos, "projeto")
                if projeto:
                    print(f"\nTarefas do projeto '{projeto.nome}':")
                    projeto.listar_tarefas()

        elif opcao == "6":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                projeto = escolher_item(gestor.projetos, "projeto")
                if projeto:
                    projeto.listar_tarefas()
                    if projeto.tarefas:
                        idx = input_int("Escolha o número da tarefa para atualizar status (ou 0 cancelar): ", minimo=0, maximo=len(projeto.tarefas))
                        if idx == 0:
                            continue
                        tarefa = projeto.tarefas[idx - 1]
                        novo = input("Novo status (Pendente/Em andamento/Concluída): ").strip()
                        if novo:
                            tarefa.atualizar_status(novo)
                            print("Status atualizado.")
                        else:
                            print("Status vazio. Cancelado.")

        elif opcao == "7":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                projeto = escolher_item(gestor.projetos, "projeto")
                if projeto:
                    projeto.listar_tarefas()
                    if projeto.tarefas:
                        idx = input_int("Escolha o número da tarefa para editar (ou 0 cancelar): ", minimo=0, maximo=len(projeto.tarefas))
                        if idx == 0:
                            continue
                        tarefa = projeto.tarefas[idx - 1]
                        novo_nome = input(f"Novo nome [{tarefa.nome}] (Enter = manter): ").strip() or None
                        nova_desc = input(f"Nova descrição (Enter = manter): ").strip() or None
                        nova_prio = input(f"Nova prioridade (Baixa/Média/Alta) [{tarefa.prioridade}] (Enter = manter): ").strip() or None
                        prazo_str = input("Novo prazo (dd/mm/aaaa) ou Enter para manter/remover: ").strip()
                        if prazo_str == "":
                            novo_prazo = None  # manter
                        else:
                            novo_prazo = parse_date(prazo_str)
                            if novo_prazo is None:
                                print("Formato de data inválido. Edição cancelada.")
                                continue
                        tarefa.atualizar_dados(nome=novo_nome, descricao=nova_desc, prioridade=nova_prio, prazo=novo_prazo)
                        print("Tarefa atualizada com sucesso.")

        elif opcao == "8":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                print(f"\nTodas as tarefas do gestor {gestor.nome}:")
                gestor.listar_todas_tarefas()

        elif opcao == "9":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                projeto = escolher_item(gestor.projetos, "projeto")
                if projeto:
                    confirm = input(f"Confirma exclusão do projeto '{projeto.nome}'? (s/N): ").strip().lower()
                    if confirm == "s":
                        gestor.remover_projeto(projeto)
                        print("Projeto excluído.")
                    else:
                        print("Cancelado.")

        elif opcao == "10":
            gestor = escolher_item(gestores, "gestor")
            if gestor:
                projeto = escolher_item(gestor.projetos, "projeto")
                if projeto:
                    projeto.listar_tarefas()
                    if projeto.tarefas:
                        idx = input_int("Escolha o número da tarefa para excluir (ou 0 cancelar): ", minimo=0, maximo=len(projeto.tarefas))
                        if idx == 0:
                            continue
                        tarefa = projeto.tarefas[idx - 1]
                        confirm = input(f"Confirma exclusão da tarefa '{tarefa.nome}'? (s/N): ").strip().lower()
                        if confirm == "s":
                            projeto.remover_tarefa(tarefa)
                            print("Tarefa excluída.")
                        else:
                            print("Cancelado.")

        elif opcao == "0":
            print("Saindo... até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main_loop()
