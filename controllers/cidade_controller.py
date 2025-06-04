import pandas as pd
from models.cidade import Cidade

class CidadeController:
    def __init__(self):
        self.cidades = []
    
    def adicionar_cidade(self, nome, dimensao, populacao):
        nova_cidade = Cidade(nome, dimensao, populacao)
        self.cidades.append(nova_cidade)
        return nova_cidade
    
    def listar_cidades(self, filtro=None):
        if filtro:
            return [c for c in self.cidades if filtro.lower() in c.nome.lower()]
        return self.cidades
    
    def buscar_por_nome(self, nome):
        for cidade in self.cidades:
            if cidade.nome.lower() == nome.lower():
                return cidade
        return None
    
    def atualizar_cidade(self, nome_antigo, novos_dados):
        cidade = self.buscar_por_nome(nome_antigo)
        if cidade:
            cidade.nome = novos_dados.get('nome', cidade.nome)
            cidade.dimensao = novos_dados.get('dimensao', cidade.dimensao)
            cidade.populacao = novos_dados.get('populacao', cidade.populacao)
            return True
        return False
    
    def remover_cidade(self, nome):
        cidade = self.buscar_por_nome(nome)
        if cidade:
            self.cidades.remove(cidade)
            return True
        return False
    
    def importar_excel(self, caminho_arquivo):
        try:
            df = pd.read_excel(caminho_arquivo, engine="openpyxl")
            required_columns = {'nome', 'dimensao', 'populacao'}
            if not required_columns.issubset(df.columns):
                return False, "O arquivo precisa ter as colunas: nome, dimensao, populacao"
            
            novas_cidades = []
            for _, row in df.iterrows():
                nova_cidade = Cidade(row["nome"], row["dimensao"], row["populacao"])
                novas_cidades.append(nova_cidade)
            
            self.cidades.extend(novas_cidades)
            return True, f"{len(novas_cidades)} cidades importadas."
        except Exception as e:
            return False, str(e)
    
    def cidade_mais_extensa(self):
        if not self.cidades:
            return None
        return max(self.cidades, key=lambda c: c.dimensao)
    
    def cidade_mais_populosa(self):
        if not self.cidades:
            return None
        return max(self.cidades, key=lambda c: c.populacao)
    
    def media_populacao(self):
        if not self.cidades:
            return 0
        return sum(c.populacao for c in self.cidades) / len(self.cidades)