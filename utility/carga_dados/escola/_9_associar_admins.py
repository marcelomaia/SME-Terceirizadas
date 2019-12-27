import datetime

from des.models import DynamicEmailConfiguration

from sme_terceirizadas.escola.models import Escola, DiretoriaRegional, Codae
from sme_terceirizadas.perfil.models import Perfil, Usuario, Vinculo

data_atual = datetime.date.today()

usuario_escola = Usuario.objects.get(email='escola@admin.com')
usuario_escola.registro_funcional = '0000001'
usuario_escola.nome = 'SUPER USUARIO ESCOLA'
usuario_escola.save()
usuario_dre = Usuario.objects.get(email='dre@admin.com')
usuario_dre.registro_funcional = '0000010'
usuario_dre.nome = 'SUPER USUARIO DRE'
usuario_dre.save()
usuario_codae = Usuario.objects.get(email='codae@admin.com')
usuario_codae.registro_funcional = '0000011'
usuario_codae.nome = 'SUPER USUARIO CODAE'
usuario_codae.save()
usuario_terceirizada = Usuario.objects.get(email='terceirizada@admin.com')
usuario_terceirizada.registro_funcional = '0000100'
usuario_terceirizada.nome = 'SUPER USUARIO TERCEIRIZADA'
usuario_terceirizada.save()
usuario_nutri_codae = Usuario.objects.get(email='nutricodae@admin.com')
usuario_nutri_codae.registro_funcional = '0000101'
usuario_nutri_codae.nome = 'USUARIO NUTRICIONISTA CODAE'
usuario_nutri_codae.save()

perfil_diretor_escola, created = Perfil.objects.get_or_create(
    nome='DIRETOR',
    ativo=True,
    super_usuario=True
)

perfil_administrador_escola, created = Perfil.objects.get_or_create(
    nome='ADMINISTRADOR_ESCOLA',
    ativo=True,
    super_usuario=True
)

perfil_cogestor_dre, created = Perfil.objects.get_or_create(
    nome='COGESTOR',
    ativo=True,
    super_usuario=True
)

perfil_administrador_diretoria_regional, created = Perfil.objects.get_or_create(
    nome='ADMINISTRADOR_DRE',
    ativo=True,
    super_usuario=True
)

perfil_usuario_nutri_codae, created = Perfil.objects.get_or_create(
    nome='COORDENADOR_DIETA_ESPECIAL',
    ativo=True,
    super_usuario=True
)

Perfil.objects.get_or_create(
    nome='ADMINISTRADOR_DIETA_ESPECIAL',
    ativo=True,
    super_usuario=True
)

perfil_usuario_codae, created = Perfil.objects.get_or_create(
    nome='COORDENADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA',
    ativo=True,
    super_usuario=True
)

Perfil.objects.get_or_create(
    nome='ADMINISTRADOR_GESTAO_ALIMENTACAO_TERCEIRIZADA',
    ativo=True,
    super_usuario=True
)

perfil_usuario_terceirizada, created = Perfil.objects.get_or_create(
    nome='NUTRI_ADMIN_RESPONSAVEL',
    ativo=True,
    super_usuario=True
)

Perfil.objects.get_or_create(
    nome='ADMINISTRADOR_TERCEIRIZADA',
    ativo=True,
    super_usuario=True
)


escola = Escola.objects.get(nome='EMEF JOSE ERMIRIO DE MORAIS, SEN.')
diretoria_regional = DiretoriaRegional.objects.get(nome='DIRETORIA REGIONAL DE EDUCACAO SAO MIGUEL')
codae, created = Codae.objects.get_or_create(nome='CODAE')
terceirizada = escola.lote.terceirizada

Vinculo.objects.create(
    instituicao=escola,
    perfil=perfil_diretor_escola,
    usuario=usuario_escola,
    data_inicial=data_atual
)
print(f'perfil {perfil_diretor_escola.nome} vinculado a {escola.nome} com sucesso')

Vinculo.objects.create(
    instituicao=diretoria_regional,
    perfil=perfil_cogestor_dre,
    usuario=usuario_dre,
    data_inicial=data_atual
)
print(f'perfil {perfil_cogestor_dre.nome} vinculado a {diretoria_regional.nome} com sucesso')

Vinculo.objects.create(
    instituicao=codae,
    perfil=perfil_usuario_codae,
    usuario=usuario_codae,
    data_inicial=data_atual
)
print(f'perfil {perfil_usuario_codae.nome} vinculado a {codae.nome} com sucesso')

Vinculo.objects.create(
    instituicao=codae,
    perfil=perfil_usuario_nutri_codae,
    usuario=usuario_nutri_codae,
    data_inicial=data_atual
)
print(f'perfil {perfil_usuario_nutri_codae.nome} vinculado a {codae.nome} com sucesso')

Vinculo.objects.create(
    instituicao=terceirizada,
    perfil=perfil_usuario_terceirizada,
    usuario=usuario_terceirizada,
    data_inicial=data_atual
)
print(f'perfil {perfil_usuario_terceirizada.nome} vinculado a {terceirizada.nome_fantasia} com sucesso')

print('Criando configuração default de email')

import os
DynamicEmailConfiguration.objects.create(
    host=os.environ['EMAIL_HOST'],
    port=os.environ['EMAIL_PORT'],
    from_email=os.environ['EMAIL_HOST_USER'],
    username=os.environ['EMAIL_HOST_USER'],
    password=os.environ['EMAIL_HOST_PASSWORD'],
    use_tls=os.environ['EMAIL_USE_TLS'],
    timeout=60
)
