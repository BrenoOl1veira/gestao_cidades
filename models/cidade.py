class Cidade:
    def __init__(self, nome, dimensao, populacao):
        self.nome = nome.strip().title()
        self.dimensao = float(dimensao)
        self.populacao = int(populacao)
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'dimensao': self.dimensao,
            'populacao': self.populacao
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['nome'], data['dimensao'], data['populacao'])