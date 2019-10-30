from notifications.models import Notification
from rest_framework import serializers

from ...escola.api.validators import usuario_e_vinculado_a_aquela_instituicao
from ...eol_servico.utils import get_informacoes_usuario
from .validators import (
    deve_ser_email_sme, registro_funcional_e_cpf_sao_da_mesma_pessoa, senha_deve_ser_igual_confirmar_senha,
    usuario_pode_efetuar_cadastro
)
from ..models import Perfil, Usuario, Vinculo


class PerfilSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('nome', 'uuid')


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        exclude = ('id', 'nome', 'ativo')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ('actor_object_id', 'target_object_id', 'action_object_object_id', 'recipient',
                   'actor_content_type', 'target_content_type', 'action_object_content_type')


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('uuid', 'nome', 'email', 'date_joined', 'registro_funcional')


class VinculoSerializer(serializers.ModelSerializer):
    perfil = PerfilSimplesSerializer()
    usuario = UsuarioSerializer()

    class Meta:
        model = Vinculo
        fields = ('uuid', 'data_inicial', 'data_final', 'perfil', 'usuario')


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    confirmar_password = serializers.CharField()

    def create(self, validated_data):
        informacoes_usuario = get_informacoes_usuario(validated_data['registro_funcional'])
        informacoes_usuario = informacoes_usuario.json()['results']
        nome_escola = validated_data.pop('escola')
        usuario_e_vinculado_a_aquela_instituicao(
            instituicao_objeto=nome_escola,
            instituicoes_eol=informacoes_usuario
        )
        cpf = informacoes_usuario[0]['cd_cpf_pessoa']
        if Usuario.objects.filter(cpf=cpf).exists():
            usuario = Usuario.objects.get(cpf=cpf)
        else:
            email = f'{cpf}@dev.prefeitura.sp.gov.br'
            usuario = Usuario.objects.create_user(email, 'adminadmin')
        usuario.registro_funcional = validated_data['registro_funcional']
        usuario.nome = informacoes_usuario[0]['nm_pessoa']
        usuario.cpf = cpf
        usuario.is_active = False
        usuario.save()
        return usuario

    def _validate(self, instance, attrs):
        senha_deve_ser_igual_confirmar_senha(attrs['password'], attrs['confirmar_password'])
        registro_funcional_e_cpf_sao_da_mesma_pessoa(instance, attrs['registro_funcional'], attrs['cpf'])
        usuario_pode_efetuar_cadastro(instance)
        deve_ser_email_sme(attrs['email'])
        return attrs

    def partial_update(self, instance, validated_data):
        validated_data = self._validate(instance, validated_data)
        self.update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = Usuario
        fields = ('email', 'registro_funcional', 'password', 'confirmar_password', 'cpf')
        write_only_fields = ('password',)
