import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Painel CODIN", layout="wide", page_icon="📊")

# --- CSS customizado para os cartões de KPI e status ---
st.markdown("""
<style>
    .kpi-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .kpi-card-red {
        border-left: 8px solid #DC2626;
    }
    .kpi-card-blue {
        border-left: 8px solid #1E3A8A;
    }
    .kpi-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #555;
        margin: 0;
        font-weight: 500;
    }
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 5px;
    }
    .status-critico { background-color: #fecaca; color: #991b1b; border: 1px solid #dc2626; }
    .status-regular { background-color: #bbf7d0; color: #14532d; border: 1px solid #22c55e; }
    .status-ativo   { background-color: #bfdbfe; color: #1e3a8a; border: 1px solid #3b82f6; }
    .status-inativo { background-color: #e5e7eb; color: #374151; border: 1px solid #9ca3af; }
</style>
""", unsafe_allow_html=True)

# --- Dados extraídos do PDF ---
# KPI Globais
kpis = {
    "Total Reuniões (2026)": 23,
    "Mandatos Vencidos": 2,
    "Vacâncias": 2,
    "Nomeações em Andamento": 2
}

# Dados de cada colegiado
colegiados = [
    {
        "nome": "Assembleia Geral",
        "status": "Ativo",
        "ultima_reuniao": "20/07/2026",
        "reunioes_2026": 1,
        "mandato": "N/A",
        "vacancia": "Não",
        "membros": ["SECC", "IVB", "CEHAB"],
        "processo": "SEISEI-220003/001002/2026",
        "detalhes": {
            "Natureza": "Órgão máximo de deliberação da Companhia; decisões de competência dos acionistas (ES, Art. 33)",
            "Composição": "Acionistas com direito a voto; trabalhos conduzidos pelo Diretor-Presidente ou substituto",
            "Convocação": "Conselho de Administração (regra geral); subsidiariamente Diretoria, CF ou acionistas (ES, Art. 12)",
            "Presidência": "Acionista Majoritário / Governo do RJ (art. 9 - ES)",
            "Quem define a pauta": "Definida no edital de convocação (documento criado para convocar) – pauta fechada (ES, Art. 12, §3º)",
            "Periodicidade": "Ordinariamente 1x/ano (até 30/04); extraordinariamente quando necessário",
            "Quorum": "1ª convocação: ≥25% do capital votante; 2ª convocação: qualquer número (ES, Art. 11)",
            "Secretaria Executiva": "Chefia de Gabinete (Art. 40 RI)",
            "Quem lavra a Ata": "Secretário escolhido entre os acionistas presentes (ES, Art. 9º). Registrada em livro de atas (pode ser sumária)",
            "Atribuições": "Alteração do capital social; avaliação de bens; transformação, fusão, incorporação, cisão, dissolução e liquidação; eleição e destituição dos membros do CA e CF; fixação da remuneração; aprovação do relatório anual; alteração do Estatuto Social (AGE).",
            "Prazos e Formalidades": "Convocação: 8 dias (1ª); Quórum: 25% (1ª) / qualquer (2ª); Deliberações: maioria do capital votante"
        },
        "publicacao": "JUCERJ",
        "base_legal": "Lei 6.404/1976; Lei 13.303/2016; art. 8º ES; arts. 37 e 137 da CF"
    },
    {
        "nome": "Conselho de Administração",
        "status": "CRÍTICO",
        "ultima_reuniao": "03/07/2026",
        "reunioes_2026": 6,
        "mandato": "VENCIDO (11/12/25)",
        "vacancia": "Sim / Em andamento",
        "membros": ["THOMPSON LEMOS SILVA NETO", "ANDERSON CARLOS MATTOS", "JORGE LUIZ TEIXEIRA CAVALCANTE", "LUIZ CLAUDIO ALMEIDA MAGALHÃES"],
        "processo": "SEISEI-220010/000165/2023",
        "detalhes": {
            "Natureza": "Órgão colegiado de orientação estratégica e supervisão",
            "Composição": "3 membros (1 Presidente: SEDEICS); 2 (1 Vice: SEFAZ); 1 (SEAPPA); 1 minoritário; 1 independente",
            "Convocação": "Pelo Presidente ou por dois conselheiros, com antecedência mínima de 5 dias",
            "Presidência": "Representante da SEDEICS ou da SECC (inciso I, art. 34 - ES)",
            "Quem define a pauta": "Presidente do CA, com base nas matérias da ordem do dia",
            "Periodicidade": "Ordinariamente conforme calendário, no mínimo trimestral; extraordinariamente quando necessário",
            "Quorum": "Maioria dos seus membros (art. 39 ES)",
            "Secretaria Executiva": "Chefia de Gabinete (CHEGAB)",
            "Quem lavra a Ata": "Secretariada pela Chefia de Gabinete; deliberações registradas no Livro de Atas do CA (RI, Art. 40, IX)",
            "Atribuições": "Definir diretrizes estratégicas; eleger e destituir a Diretoria Executiva; fiscalizar a gestão; aprovar políticas, plano de negócios, orçamento, gestão de riscos, auditoria, regimentos e matérias patrimoniais relevantes",
            "Prazos e Formalidades": "Convocação: 5 dias por escrito; Periodicidade mínima: trimestral; Quórum: maioria; Deliberações: maioria de votos (voto de qualidade do Presidente em caso de empate - ES, Art. 20, Par. 3°)"
        },
        "publicacao": "JUCERJ",
        "base_legal": "Lei 6.404/1976; Lei 13.303/2016; art. 33º ES; arts. 37 e 137 da CF"
    },
    {
        "nome": "Diretoria Executiva",
        "status": "Regular",
        "ultima_reuniao": "07/07/2026",
        "reunioes_2026": 3,
        "mandato": "Em dia",
        "vacancia": "Não",
        "membros": ["Luiz Eduardo (DIRIF)", "Andreia (DIRNN)","Carla (PRESI)"],
        "processo": "SEI-150001/005343/2026; SEI-220003/000960/2026; SEI-220003/001074/2026",
        "detalhes": {
            "Natureza": "Órgão executivo responsável pela administração da Companhia",
            "Composição": "Diretor-Presidente e até cinco Diretores, mínimo de três",
            "Convocação": "Pelo Diretor-Presidente ou por três Diretores",
            "Presidência": "Diretor-Presidente (§ 1º, art. 45 ES)",
            "Quem define a pauta": "Diretor-Presidente, considerando matérias submetidas pelos Diretores e unidades técnicas",
            "Periodicidade": "Ordinariamente, pelo menos uma vez a cada dois meses; extraordinariamente quando necessário",
            "Quorum": "Maioria absoluta (§ 4º, art. 45 ES)",
            "Secretaria Executiva": "Não informado",
            "Quem lavra a Ata": "Chefe de Gabinete",
            "Atribuições": "Executar as diretrizes do Conselho; administrar a Companhia; elaborar orçamento e plano de negócios; gerir contratos, patrimônio e pessoal; representar a Companhia",
            "Prazos e Formalidades": "Não informado"
        },
        "publicacao": "Não informado",
        "base_legal": "Lei 6.404/1976; Lei 13.303/2016; art. 41º Estatuto Social"
    },
    {
        "nome": "Conselho Fiscal",
        "status": "CRÍTICO",
        "ultima_reuniao": "25/06/2026",
        "reunioes_2026": 7,
        "mandato": "VENCIDO (11/12/25)",
        "vacancia": "Sim (SEDEICS vago)",
        "membros": ["Gabriel Mac-Dowell Blum (Presidente)", "Francisco Pereira Iglesias", "VAGO (SEDEICS)"],
        "processo": "SEISEI-220010/000165/2023",
        "detalhes": {
            "Natureza": "Órgão permanente de fiscalização",
            "Composição": "2 efetivos + suplentes (1 da SEFAZ); 1 efetivo + suplente (SEDEICS); 1 efetivo + suplente (acionistas minoritários)",
            "Convocação": "Pelo Conselheiro Presidente",
            "Presidência": "Escolhido na primeira reunião após a eleição, de comum acordo (ES, Art. 52, §2º)",
            "Quem define a pauta": "Presidente do CF, com base nas matérias de fiscalização e análise periódica",
            "Periodicidade": "Mensal; extraordinárias quando necessário",
            "Quorum": "Maioria dos membros",
            "Secretaria Executiva": "Designado pela presidência (ES, Art. 58, §único)",
            "Quem lavra a Ata": "Não informado",
            "Atribuições": "Fiscalizar os atos da administração; examinar demonstrações financeiras; opinar sobre matérias societárias relevantes; comunicar irregularidades",
            "Prazos e Formalidades": "Periodicidade ordinária: mensal; Quórum: maioria; Análise financeira: trimestral; Mandato: 2 anos (máx. 2 reconduções); Remuneração: fixada pela AG (< 15% da média mensal da Diretoria)"
        },
        "publicacao": "JUCERJ",
        "base_legal": "Lei 6.404/1976; Lei 13.303/2016; Decreto Estadual 45.188/2017; art. 33º ES; arts. 37 e 137 da CF. Aplica-se subsidiariamente a Lei 6.404/76 e Dec. Est. 46.188/2017"
    },
    {
        "nome": "Comitê de Auditoria",
        "status": "Inativo",
        "ultima_reuniao": "Não realizada",
        "reunioes_2026": 0,
        "mandato": "Sem dados",
        "vacancia": "N/A",
        "membros": ["3 independentes (não informado)"],
        "processo": "Não informado",
        "detalhes": {
            "Natureza": "Órgão de assessoramento ao Conselho de Administração",
            "Composição": "Três membros independentes eleitos e destituídos pelo CA; Prazo de gestão: 03 anos; Permitida uma recondução",
            "Convocação": "Não informado",
            "Presidência": "Escolhido na primeira reunião após a eleição, de comum acordo (ES, Art. 61, Súnico)",
            "Quem define a pauta": "Não informado",
            "Periodicidade": "Bimestral",
            "Quorum": "Não informado",
            "Secretaria Executiva": "Não informado",
            "Quem lavra a Ata": "Não informado",
            "Atribuições": "Supervisionar auditorias interna e externa; monitorar controles internos e gestão de riscos; acompanhar demonstrações financeiras; receber denúncias e elaborar relatório anual",
            "Prazos e Formalidades": "Não informado"
        },
        "publicacao": "Não informado",
        "base_legal": "Lei 13.303/2016; Decreto Estadual 45.188/2017; art. 62º Estatuto Social"
    },
    {
        "nome": "Comitê de Elegibilidade",
        "status": "Regular",
        "ultima_reuniao": "20/05/2026",
        "reunioes_2026": 6,
        "mandato": "Em dia",
        "vacancia": "Eleição por revogação",
        "membros": ["Carla Amanda de Souza Carneiro", "Carla Pereira", "Maria Izete de Oliveira"],
        "processo": "SEISEI-220010/000297/2022",
        "detalhes": {
            "Natureza": "Órgão de assessoramento responsável pela análise de elegibilidade",
            "Composição": "Três membros, preferencialmente do Comitê de Auditoria, empregados ou conselheiros",
            "Convocação": "Pelo seu Presidente, ou dois de seus membros, por intermédio da Chefia de Gabinete, com antecedência mínima de 07 dias",
            "Presidência": "O Presidente será eleito entre seus membros (Art. 7º § 1º)",
            "Quem define a pauta": "Não informado",
            "Periodicidade": "Conforme necessidade",
            "Quorum": "2 membros",
            "Secretaria Executiva": "Não informado",
            "Quem lavra a Ata": "O CAE é responsável pela elaboração das atas (Art. 17º § 2º RI)",
            "Atribuições": "Verificar requisitos legais para nomeações; analisar impedimentos; emitir pareceres sobre indicações; avaliar conformidade dos processos de escolha",
            "Prazos e Formalidades": "É obrigatória a participação do CAE nas reuniões ordinárias do Conselho de Administração"
        },
        "publicacao": "DOERJ",
        "base_legal": "Arts. 156 e 165 da Lei 6.404/1976; art. 69 do Estatuto Social"
    }
]

# --- Funções auxiliares ---
def get_status_class(status):
    if "crítico" in status.lower():
        return "status-critico"
    elif "regular" in status.lower():
        return "status-regular"
    elif "ativo" in status.lower():
        return "status-ativo"
    elif "inativo" in status.lower():
        return "status-inativo"
    return "status-regular"

# --- Cabeçalho ---
st.title("📊 Painel de Governança - CODIN")
st.caption("Base: 24/07/2026")
st.markdown("---")

# --- KPIs Globais ---
cols = st.columns(4)
with cols[0]:
    st.markdown(f"""
    <div class="kpi-card kpi-card-blue">
        <div class="kpi-number">{kpis['Total Reuniões (2026)']}</div>
        <div class="kpi-label">Total Reuniões (2026)</div>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown(f"""
    <div class="kpi-card kpi-card-red">
        <div class="kpi-number">{kpis['Mandatos Vencidos']}</div>
        <div class="kpi-label">Mandatos Vencidos</div>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown(f"""
    <div class="kpi-card kpi-card-red">
        <div class="kpi-number">{kpis['Vacâncias']}</div>
        <div class="kpi-label">Vacâncias</div>
    </div>
    """, unsafe_allow_html=True)
with cols[3]:
    st.markdown(f"""
    <div class="kpi-card kpi-card-blue">
        <div class="kpi-number">{kpis['Nomeações em Andamento']}</div>
        <div class="kpi-label">Nomeações em Andamento</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Detalhamento dos Colegiados ---
st.subheader("📋 Detalhamento dos Colegiados")

for org in colegiados:
    status_color = get_status_class(org['status'])
    
    # Card principal
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"### {org['nome']}")
            st.markdown(f"<span class='status-badge {status_color}'>{org['status']}</span>", unsafe_allow_html=True)
            
            st.markdown(f"**Última Reunião:** {org['ultima_reuniao']}")
            st.markdown(f"**Reuniões (2026):** {org['reunioes_2026']}")
            st.markdown(f"**Mandato:** {org['mandato']}")
            st.markdown(f"**Vacância:** {org['vacancia']}")
            
            if org['membros']:
                st.markdown(f"**Membros:**")
                for m in org['membros']:
                    st.markdown(f"- {m}")
        
        with col2:
            # Detalhes expandíveis
            with st.expander("📌 Ver detalhes completos"):
                # Informações gerais
                if org['processo']:
                    st.markdown(f"**Processo SEI:** {org['processo']}")
                if org['publicacao']:
                    st.markdown(f"**Publicação Obrigatória:** {org['publicacao']}")
                if org['base_legal']:
                    st.markdown(f"**Base Legal:** {org['base_legal']}")
                
                st.markdown("---")
                
                # Detalhes específicos do órgão
                for key, value in org['detalhes'].items():
                    st.markdown(f"**{key}:**")
                    st.markdown(f"{value}")