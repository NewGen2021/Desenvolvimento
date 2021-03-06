'''
    ('O QUE É GRAVADO NO BANCO', 'O QUE APARECE DE ESCOLHA PRO USUÁRIO')
'''
from django.utils.translation import gettext as _

SEXO_CHOICES = (
        (_("F"), _("Feminino")),
        (_("M"), _("Masculino")),
        (_("O"), _("Outro"))
    )

ESTADO_CHOICES = (
    ('AC', 'Acre'), 
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernanbuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins')
)

ESCOLHAS_ESTADOS = (('', '----------'),) + ESTADO_CHOICES

EQUIPAMENTOS_STATUS_CHOICES = (
        (0, _("Ativo")),
        (1, _("Desativado")),
        (2, _("Extraviado"))
)

PAGAMENTO_METODO_CHOICES = (
        ("PIX", _("PIX")),
        ("Cartão de Crédito", _("Cartão de Crédito")),
        ("Boleto", _("Boleto"))
    )

# PAGAMENTO_STATUS_CHOICES = (
#     (0, _("Aguardando Pagamento")),
#     (1, _("Pagamento Aprovado")),
#     (2, _("Pagamento Negado")),
#     (3, _("Pacote de Horas")),
#     (4, _("Cancelado pelo Cliente")),
#     (5, _("Expirado")),
#     (6, _("Cancelado via Sistema"))
# )

PAGAMENTO_STATUS_CHOICES = (
    (0, 400),
    (0, _("failed")),
    (1, _("approved")),
    (2, _("authorized")),
    (3, _("rejected")),
    (4, _("pending")),
    (5, _("in_process")),
    (6, _("in_mediation")),
    (7, _("refunded")),
    (8, _("charged_back")),
    (9, _("rejected")),
)

ESPACOS_STATUS_CHOICES = (
        (1, _("Ativo")),
        (0, _("Desativado"))
)