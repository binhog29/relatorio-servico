from flask import Flask, render_template, request
import datetime
from datetime import date

app = Flask(__name__)

def is_numeric_and_positive(value):
    """Verifica se o valor é um número (string) e se é maior que zero."""
    if value and value.strip().isdigit() and int(value.strip()) > 0:
        return True
    return False

def gerar_relatorio(form):
    """Gera o texto do relatório com base nos dados do formulário."""
    tipo_servico = form.get('tipo_servico', 'Serviço Não Especificado').upper()
    cliente = form.get('cliente', '').upper()
    
    # ----------------------------------------------------
    # ORDEM CORRIGIDA: Tipo de Serviço (Assunto) primeiro, depois Cliente
    # ----------------------------------------------------
    relatorio = f"SERVIÇO: {tipo_servico}\n"
    if cliente and tipo_servico != 'SERVIÇO EM TORRES':
        relatorio += f"CLIENTE: {cliente}\n"

    # ==================================
    # Variável de Observação Global
    # ==================================
    observacoes = form.get('observacoes', '').strip().upper()
    
    # ==================================
    # CAMPOS GERAIS PARA INSTALAÇÃO/MIGRAÇÃO FIBRA
    # ==================================
    if tipo_servico in ['INSTALAÇÃO FIBRA ÓPTICA', 'MIGRAÇÃO FIBRA ÓPTICA']:
        # Material
        cabo_fibra = form.get('cabo_quantidade_fibra')
        conector_fibra = form.get('conector_quantidade_fibra')
        adaptador_fibra = form.get('adaptador_quantidade_fibra')
        alcas_fibra = form.get('alcas_fibra')
        
        relatorio += "\nMATERIAL UTILIZADO:\n"
        if is_numeric_and_positive(cabo_fibra):
            relatorio += f"- {cabo_fibra} METROS DE DROP\n"
        if is_numeric_and_positive(conector_fibra):
            relatorio += f"- {conector_fibra} CONECTORES VERDES\n"
        if is_numeric_and_positive(adaptador_fibra):
            relatorio += f"- {adaptador_fibra} ACOPLADORES/EMENDAS\n"
        if is_numeric_and_positive(alcas_fibra):
            relatorio += f"- {alcas_fibra} ALÇAS\n"
        
        # Equipamento
        onu_ont = form.get('onu_ont', '').upper() 
        pon = form.get('pon', '').upper()
        smart_pro_tv_box = form.get('smart_pro_tv_box')

        relatorio += "\nEQUIPAMENTO:\n"
        if onu_ont:
            relatorio += f"- ONU/ONT (MODELO): {onu_ont}\n" 
        if pon:
            relatorio += f"- PON (SERIAL): {pon}\n"
        if is_numeric_and_positive(smart_pro_tv_box):
            relatorio += f"- {smart_pro_tv_box} SMART PRO TV BOX\n"
        
        # REMOVIDO: A observação automática para MIGRAÇÃO FIBRA ÓPTICA
        # Agora, a observação será incluída apenas se o usuário preencher o campo.

    # ==================================
    # CAMPOS PARA INSTALAÇÃO VIA RÁDIO
    # ==================================
    elif tipo_servico == 'INSTALAÇÃO VIA RÁDIO':
        # Material
        cabo_radio = form.get('cabo_quantidade_radio')
        conector_radio = form.get('conector_quantidade_radio')
        adaptador_radio = form.get('adaptador_quantidade_radio')
        alcas_radio = form.get('alcas_radio')
        
        relatorio += "\nMATERIAL UTILIZADO:\n"
        if is_numeric_and_positive(cabo_radio):
            relatorio += f"- {cabo_radio} METROS DE CABO DE REDE\n"
        if is_numeric_and_positive(conector_radio):
            relatorio += f"- {conector_radio} CONECTORES RJ-45\n"
        if is_numeric_and_positive(adaptador_radio):
            relatorio += f"- {adaptador_radio} ACOPLADORES/EMENDAS\n"
        if is_numeric_and_positive(alcas_radio):
            relatorio += f"- {alcas_radio} ALÇAS\n"
        
        # Equipamento
        roteador = form.get('roteador', '').upper()
        antena = form.get('antena', '').upper()
        smart_pro_tv_box = form.get('smart_pro_tv_box')

        relatorio += "\nEQUIPAMENTO:\n"
        if roteador:
            relatorio += f"- ROTEADOR: {roteador}\n"
        if antena:
            relatorio += f"- ANTENA: {antena}\n"
        if is_numeric_and_positive(smart_pro_tv_box):
            relatorio += f"- {smart_pro_tv_box} SMART PRO TV BOX\n"

    # ==================================
    # CAMPOS PARA SERVIÇO EM TORRES
    # ==================================
    elif tipo_servico == 'SERVIÇO EM TORRES':
        numero_torre = form.get('numero_torre', '').upper()
        relatorio = f"SERVIÇO: {tipo_servico}\n" 
        relatorio += f"LOCAL: {numero_torre}\n"

        # Material
        cabo_quantidade_torre = form.get('cabo_quantidade_torre')
        cabo_tipo_torre = form.get('cabo_tipo_torre', '').upper()
        conector_quantidade_torre = form.get('conector_quantidade_torre')
        conector_tipo_torre = form.get('conector_tipo_torre', '').upper()
        adaptador_quantidade_torre = form.get('adaptador_quantidade_torre')
        alcas_torre = form.get('alcas_torre')
        outros_equipamentos_torre = form.get('outros_equipamentos_torre', '').upper()

        relatorio += "\nMATERIAL/EQUIPAMENTO:\n"
        if is_numeric_and_positive(cabo_quantidade_torre):
            relatorio += f"- {cabo_quantidade_torre} METROS DE {cabo_tipo_torre}\n"
        if is_numeric_and_positive(conector_quantidade_torre):
            relatorio += f"- {conector_quantidade_torre} {conector_tipo_torre}\n"
        if is_numeric_and_positive(adaptador_quantidade_torre):
            relatorio += f"- {adaptador_quantidade_torre} ACOPLADORES/EMENDAS\n"
        if is_numeric_and_positive(alcas_torre):
            relatorio += f"- {alcas_torre} ALÇAS\n"
        if outros_equipamentos_torre:
            relatorio += f"- OUTROS: {outros_equipamentos_torre}\n"

    # ==================================
    # CAMPOS PARA MANUTENÇÃO/MUDANÇA/LENTIDÃO/SEM INTERNET
    # ==================================
    elif tipo_servico in ['MUDANÇA DE ENDEREÇO', 'LENTIDÃO', 'SEM INTERNET', 'MANUTENÇÃO']:
        # Material
        cabo_quantidade_manutencao = form.get('cabo_quantidade_manutencao')
        cabo_tipo = form.get('cabo_tipo', '').upper()
        conector_quantidade_manutencao = form.get('conector_quantidade_manutencao')
        conector_tipo = form.get('conector_tipo', '').upper()
        adaptador_quantidade_manutencao = form.get('adaptador_quantidade_manutencao')
        alcas_manutencao = form.get('alcas_manutencao')
        
        relatorio += "\nMATERIAL UTILIZADO:\n"
        if is_numeric_and_positive(cabo_quantidade_manutencao):
            relatorio += f"- {cabo_quantidade_manutencao} METROS DE {cabo_tipo}\n"
        if is_numeric_and_positive(conector_quantidade_manutencao):
            relatorio += f"- {conector_quantidade_manutencao} {conector_tipo}\n"
        if is_numeric_and_positive(adaptador_quantidade_manutencao):
            relatorio += f"- {adaptador_quantidade_manutencao} ACOPLADORES/EMENDAS\n"
        if is_numeric_and_positive(alcas_manutencao):
            relatorio += f"- {alcas_manutencao} ALÇAS\n"

        # Equipamento (Só para Mudança e Manutenção)
        if tipo_servico in ['MUDANÇA DE ENDEREÇO', 'MANUTENÇÃO']:
            onu_ont_manutencao = form.get('onu_ont_manutencao', '').upper() 
            pon_manutencao = form.get('pon_manutencao', '').upper()
            smart_pro_tv_box_manutencao = form.get('smart_pro_tv_box_manutencao')

            relatorio += "\nEQUIPAMENTO:\n"
            if onu_ont_manutencao:
                relatorio += f"- ONU/ONT (MODELO): {onu_ont_manutencao}\n" 
            if pon_manutencao:
                relatorio += f"- PON (SERIAL): {pon_manutencao}\n"
            if is_numeric_and_positive(smart_pro_tv_box_manutencao):
                relatorio += f"- {smart_pro_tv_box_manutencao} SMART PRO TV BOX\n"
            
    # ==================================
    # CAMPOS PARA TROCA DE EQUIPAMENTO
    # ==================================
    elif tipo_servico == 'TROCA DE EQUIPAMENTO':
        mac_retirado = form.get('mac_retirado', '').upper()
        mac_novo = form.get('mac_novo', '').upper()

        relatorio += "\nEQUIPAMENTO TROCADO:\n"
        relatorio += f"- MAC/SERIAL RETIRADO: {mac_retirado}\n"
        relatorio += f"- MAC/SERIAL NOVO: {mac_novo}\n"
        
    # ==================================
    # NOVOS CAMPOS PARA RETIRADA DE EQUIPAMENTOS
    # ==================================
    elif tipo_servico == 'RETIRADA DE EQUIPAMENTOS':
        mac_retirado_retirada = form.get('mac_retirado_retirada', '').upper()
        smart_tv_box_retirada = form.get('smart_tv_box_retirada', '').upper()
        
        relatorio += "\nEQUIPAMENTOS RETIRADOS:\n"
        relatorio += f"- ONU/ONT/ROTEADOR (MAC/SERIAL): {mac_retirado_retirada}\n" 
        if smart_tv_box_retirada:
            relatorio += f"- SMART PRO TV BOX (SERIAL): {smart_tv_box_retirada}\n"

    # ==================================
    # OBSERVAÇÕES E DATA
    # ==================================
    
    # AQUI ESTÁ A CORREÇÃO PRINCIPAL: SÓ INCLUIR SE O CAMPO NÃO ESTIVER VAZIO
    if observacoes:
        relatorio += f"\nOBSERVAÇÕES: {observacoes}\n"

    # A data do formulário vem em YYYY-MM-DD
    data_instalacao_str = form.get('data_instalacao')
    data_formatada = ""
    try:
        data_obj = datetime.datetime.strptime(data_instalacao_str, '%Y-%m-%d').date()
        data_formatada = data_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        data_formatada = date.today().strftime('%d/%m/%Y')

    relatorio += f"\nDATA: {data_formatada}\n"
    
    return relatorio.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    relatorio = None
    if request.method == 'POST':
        try:
            relatorio = gerar_relatorio(request.form)
        except Exception as e:
            return f"<h1>Erro Interno (500)</h1><p>Ocorreu um erro no servidor: {e}</p>", 500

    return render_template('relatorio.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
