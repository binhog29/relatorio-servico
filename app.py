from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

def gerar_relatorio_servico(cliente, tipo_servico, dados_servico, data_instalacao):
    data_formatada = ""
    try:
        data_obj = datetime.datetime.strptime(data_instalacao, '%Y-%m-%d').date()
        data_formatada = data_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        data_formatada = "Data Inválida"

    relatorio = f"Assunto: {tipo_servico.upper()}\n"

    if cliente:
        relatorio += f"CLIENTE: {cliente}\n"

    if tipo_servico == 'SERVIÇO EM TORRES':
        numero_torre = dados_servico.get('numero_torre')
        if numero_torre:
            relatorio += f"TORRE: {numero_torre}\n"
    
    if tipo_servico != 'TROCA DE EQUIPAMENTO':
        relatorio += "USADO:\n"
        
        cabo_quantidade = dados_servico.get('cabo_quantidade')
        cabo_tipo = dados_servico.get('cabo_tipo')
        if cabo_quantidade and cabo_tipo:
            relatorio += f"- {cabo_quantidade} metros de {cabo_tipo}\n"
        
        conector_quantidade = dados_servico.get('conector_quantidade')
        conector_tipo = dados_servico.get('conector_tipo')
        if conector_quantidade and conector_tipo:
            relatorio += f"- {conector_quantidade} {conector_tipo}\n"

        adaptador_quantidade = dados_servico.get('adaptador_quantidade')
        if adaptador_quantidade:
            relatorio += f"- {adaptador_quantidade} Acopladores/emendas SC/APC verde\n"

        alcas = dados_servico.get('alcas')
        if alcas:
            relatorio += f"- {alcas} alças\n"
        
        onu = dados_servico.get('onu')
        pon = dados_servico.get('pon')
        roteador = dados_servico.get('roteador')
        antena = dados_servico.get('antena')
        smart_pro_tv_box_quantidade = dados_servico.get('smart_pro_tv_box_quantidade')
        outros_equipamentos = dados_servico.get('outros_equipamentos')

        if onu:
            relatorio += f"\n- ONU {onu}\n"
        if pon:
            relatorio += f"Pon: {pon}\n"
        if roteador:
            relatorio += f"\n- Roteador: {roteador}\n"
        if antena:
            relatorio += f"- Antena: {antena}\n"
        if smart_pro_tv_box_quantidade:
            relatorio += f"- SMART PRO TV BOX: {smart_pro_tv_box_quantidade}\n"
        if outros_equipamentos:
            relatorio += f"\n- Outros Equipamentos:\n{outros_equipamentos}\n"


    if tipo_servico == 'TROCA DE EQUIPAMENTO':
        relatorio += f"\nEQUIPAMENTO RETIRADO:\n"
        relatorio += f"MAC/Serial: {dados_servico.get('mac_retirado', 'Não informado')}\n"
        relatorio += f"\nEQUIPAMENTO NOVO:\n"
        relatorio += f"MAC/Serial: {dados_servico.get('mac_novo', 'Não informado')}\n"
        
    observacoes = dados_servico.get('observacoes')
    if observacoes:
        relatorio += f"\nOBSERVAÇÕES:\n{observacoes}\n"

    relatorio += f"\nDATA: {data_formatada}\n"
    return relatorio.strip()

@app.route('/', methods=['GET', 'POST'])
def relatorio_app():
    relatorio_gerado = None
    if request.method == 'POST':
        cliente_nome = request.form.get('cliente', '')
        tipo_servico = request.form.get('tipo_servico', '')
        data_instalacao = request.form.get('data_instalacao')
        
        dados_servico = {}
        dados_servico['observacoes'] = request.form.get('observacoes', '')

        if tipo_servico == 'INSTALAÇÃO FIBRA ÓPTICA':
            dados_servico['cabo_tipo'] = 'DROP'
            dados_servico['conector_tipo'] = 'conectores verdes'
            dados_servico['cabo_quantidade'] = request.form.get('cabo_quantidade_fibra')
            dados_servico['conector_quantidade'] = request.form.get('conector_quantidade_fibra')
            dados_servico['adaptador_quantidade'] = request.form.get('adaptador_quantidade_fibra')
            dados_servico['alcas'] = request.form.get('alcas_fibra')
            dados_servico['onu'] = request.form.get('onu')
            dados_servico['pon'] = request.form.get('pon')
            dados_servico['smart_pro_tv_box_quantidade'] = request.form.get('smart_pro_tv_box')
        
        elif tipo_servico == 'INSTALAÇÃO VIA RÁDIO':
            dados_servico['cabo_tipo'] = 'CABO DE REDE'
            dados_servico['conector_tipo'] = 'conectores RJ-45'
            dados_servico['cabo_quantidade'] = request.form.get('cabo_quantidade_radio')
            dados_servico['conector_quantidade'] = request.form.get('conector_quantidade_radio')
            dados_servico['adaptador_quantidade'] = request.form.get('adaptador_quantidade_radio')
            dados_servico['roteador'] = request.form.get('roteador')
            dados_servico['antena'] = request.form.get('antena')
            dados_servico['alcas'] = request.form.get('alcas_radio')
            dados_servico['smart_pro_tv_box_quantidade'] = request.form.get('smart_pro_tv_box')

        elif tipo_servico == 'MUDANÇA DE ENDEREÇO':
            dados_servico['cabo_tipo'] = 'DROP'
            dados_servico['conector_tipo'] = 'conectores verdes'
            dados_servico['cabo_quantidade'] = request.form.get('cabo_quantidade_manutencao')
            dados_servico['conector_quantidade'] = request.form.get('conector_quantidade_manutencao')
            dados_servico['adaptador_quantidade'] = request.form.get('adaptador_quantidade_manutencao')
            dados_servico['alcas'] = request.form.get('alcas_manutencao')
            dados_servico['onu'] = request.form.get('onu_manutencao')
            dados_servico['pon'] = request.form.get('pon_manutencao')
            dados_servico['smart_pro_tv_box_quantidade'] = request.form.get('smart_pro_tv_box_manutencao')
            
        elif tipo_servico in ['LENTIDÃO', 'SEM INTERNET', 'MANUTENÇÃO']:
            dados_servico['cabo_tipo'] = request.form.get('cabo_tipo')
            dados_servico['conector_tipo'] = request.form.get('conector_tipo')
            dados_servico['cabo_quantidade'] = request.form.get('cabo_quantidade_manutencao')
            dados_servico['conector_quantidade'] = request.form.get('conector_quantidade_manutencao')
            dados_servico['adaptador_quantidade'] = request.form.get('adaptador_quantidade_manutencao')
            dados_servico['alcas'] = request.form.get('alcas_manutencao')
            dados_servico['onu'] = request.form.get('onu_manutencao')
            dados_servico['pon'] = request.form.get('pon_manutencao')
            dados_servico['smart_pro_tv_box_quantidade'] = request.form.get('smart_pro_tv_box_manutencao')
            
        elif tipo_servico == 'SERVIÇO EM TORRES':
            dados_servico['numero_torre'] = request.form.get('numero_torre')
            dados_servico['cabo_tipo'] = request.form.get('cabo_tipo_torre')
            dados_servico['conector_tipo'] = request.form.get('conector_tipo_torre')
            dados_servico['cabo_quantidade'] = request.form.get('cabo_quantidade_torre')
            dados_servico['conector_quantidade'] = request.form.get('conector_quantidade_torre')
            dados_servico['adaptador_quantidade'] = request.form.get('adaptador_quantidade_torre')
            dados_servico['alcas'] = request.form.get('alcas_torre')
            dados_servico['outros_equipamentos'] = request.form.get('outros_equipamentos_torre')

        elif tipo_servico == 'TROCA DE EQUIPAMENTO':
            dados_servico['mac_retirado'] = request.form.get('mac_retirado')
            dados_servico['mac_novo'] = request.form.get('mac_novo')
        
        if cliente_nome or tipo_servico == 'SERVIÇO EM TORRES':
             relatorio_gerado = gerar_relatorio_servico(
                cliente=cliente_nome,
                tipo_servico=tipo_servico,
                dados_servico=dados_servico,
                data_instalacao=data_instalacao
            )
        
    return render_template('relatorio.html', relatorio=relatorio_gerado)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
