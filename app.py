from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

def gerar_relatorio(form):
    """Gera o texto do relatório com base nos dados do formulário."""
    tipo_servico = form.get('tipo_servico', 'Serviço Não Especificado')
    cliente = form.get('cliente', '').upper()
    data_instalacao = form.get('data_instalacao')
    
    relatorio = f"CLIENTE: {cliente}\n"
    relatorio += f"SERVIÇO: {tipo_servico}\n"

    # ==================================
    # CAMPOS GERAIS PARA INSTALAÇÃO/MIGRAÇÃO FIBRA
    # (Usado em 'INSTALAÇÃO FIBRA ÓPTICA' e 'MIGRAÇÃO FIBRA ÓPTICA')
    # ==================================
    if tipo_servico in ['INSTALAÇÃO FIBRA ÓPTICA', 'MIGRAÇÃO FIBRA ÓPTICA']:
        # Material
        cabo_fibra = form.get('cabo_quantidade_fibra')
        conector_fibra = form.get('conector_quantidade_fibra')
        adaptador_fibra = form.get('adaptador_quantidade_fibra')
        alcas_fibra = form.get('alcas_fibra')
        
        relatorio += "\nMATERIAL UTILIZADO:\n"
        if cabo_fibra and int(cabo_fibra) > 0:
            relatorio += f"- {cabo_fibra} METROS DE DROP\n"
        if conector_fibra and int(conector_fibra) > 0:
            relatorio += f"- {conector_fibra} CONECTORES VERDES\n"
        if adaptador_fibra and int(adaptador_fibra) > 0:
            relatorio += f"- {adaptador_fibra} ACOPLADORES/EMENDAS\n"
        if alcas_fibra and int(alcas_fibra) > 0:
            relatorio += f"- {alcas_fibra} ALÇAS\n"
        
        # Equipamento
        onu = form.get('onu', '').upper()
        pon = form.get('pon', '').upper()
        smart_pro_tv_box = form.get('smart_pro_tv_box')

        relatorio += "\nEQUIPAMENTO:\n"
        if onu:
            relatorio += f"- ONU (MODELO): {onu}\n"
        if pon:
            relatorio += f"- PON (SERIAL): {pon}\n"
        if smart_pro_tv_box and int(smart_pro_tv_box) > 0:
            relatorio += f"- {smart_pro_tv_box} SMART PRO TV BOX\n"
        
        # Detalhe específico para Migração
        if tipo_servico == 'MIGRAÇÃO FIBRA ÓPTICA':
            relatorio += "OBS: Foi realizada a migração de tecnologia para Fibra Óptica.\n"

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
        if cabo_radio and int(cabo_radio) > 0:
            relatorio += f"- {cabo_radio} METROS DE CABO DE REDE\n"
        if conector_radio and int(conector_radio) > 0:
            relatorio += f"- {conector_radio} CONECTORES RJ-45\n"
        if adaptador_radio and int(adaptador_radio) > 0:
            relatorio += f"- {adaptador_radio} ACOPLADORES/EMENDAS\n"
        if alcas_radio and int(alcas_radio) > 0:
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
        if smart_pro_tv_box and int(smart_pro_tv_box) > 0:
            relatorio += f"- {smart_pro_tv_box} SMART PRO TV BOX\n"

    # ==================================
    # CAMPOS PARA SERVIÇO EM TORRES
    # ==================================
    elif tipo_servico == 'SERVIÇO EM TORRES':
        numero_torre = form.get('numero_torre', '').upper()
        relatorio = relatorio.replace(f"CLIENTE: {cliente}\n", "") # Remove o cliente, que não é usado

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
        if cabo_quantidade_torre and int(cabo_quantidade_torre) > 0:
            relatorio += f"- {cabo_quantidade_torre} METROS DE {cabo_tipo_torre}\n"
        if conector_quantidade_torre and int(conector_quantidade_torre) > 0:
            relatorio += f"- {conector_quantidade_torre} {conector_tipo_torre}\n"
        if adaptador_quantidade_torre and int(adaptador_quantidade_torre) > 0:
            relatorio += f"- {adaptador_quantidade_torre} ACOPLADORES/EMENDAS\n"
        if alcas_torre and int(alcas_torre) > 0:
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
        if cabo_quantidade_manutencao and int(cabo_quantidade_manutencao) > 0:
            relatorio += f"- {cabo_quantidade_manutencao} METROS DE {cabo_tipo}\n"
        if conector_quantidade_manutencao and int(conector_quantidade_manutencao) > 0:
            relatorio += f"- {conector_quantidade_manutencao} {conector_tipo}\n"
        if adaptador_quantidade_manutencao and int(adaptador_quantidade_manutencao) > 0:
            relatorio += f"- {adaptador_quantidade_manutencao} ACOPLADORES/EMENDAS\n"
        if alcas_manutencao and int(alcas_manutencao) > 0:
            relatorio += f"- {alcas_manutencao} ALÇAS\n"

        # Equipamento (Só para Mudança e Manutenção)
        if tipo_servico in ['MUDANÇA DE ENDEREÇO', 'MANUTENÇÃO']:
            onu_manutencao = form.get('onu_manutencao', '').upper()
            pon_manutencao = form.get('pon_manutencao', '').upper()
            smart_pro_tv_box_manutencao = form.get('smart_pro_tv_box_manutencao')

            relatorio += "\nEQUIPAMENTO:\n"
            if onu_manutencao:
                relatorio += f"- ONU (MODELO): {onu_manutencao}\n"
            if pon_manutencao:
                relatorio += f"- PON (SERIAL): {pon_manutencao}\n"
            if smart_pro_tv_box_manutencao and int(smart_pro_tv_box_manutencao) > 0:
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
        relatorio += f"- ONU/ROTEADOR (MAC/SERIAL): {mac_retirado_retirada}\n"
        if smart_tv_box_retirada:
            relatorio += f"- SMART PRO TV BOX (SERIAL): {smart_tv_box_retirada}\n"

    # ==================================
    # OBSERVAÇÕES E DATA
    # ==================================
    observacoes = form.get('observacoes', '').upper()
    
    if observacoes:
        relatorio += f"\nOBSERVAÇÕES: {observacoes}\n"

    relatorio += f"\nDATA: {date.today().strftime('%d/%m/%Y')}\n"
    
    return relatorio

@app.route('/', methods=['GET', 'POST'])
def index():
    relatorio = None
    if request.method == 'POST':
        relatorio = gerar_relatorio(request.form)
    
    return render_template('relatorio.html', relatorio=relatorio)

if __name__ == '__main__':
    # Use 0.0.0.0 para que o Vercel ou Termux consiga rodar
    app.run(host='0.0.0.0', port=5000, debug=True)
