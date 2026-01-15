/* 
   LOGIC NODE: PROCESSADOR DE REGRAS DE NEGÓCIO EGE
   Entrada: JSON da IA (items)
   Saída: JSON Final para Planilha/Proposta com Preços Calculados
*/

// CONSTANTES GLOBAIS
const CONTINGENCY_PCT = 0.20; // 20% Imprevistos
const MISC_PCT = 0.10;        // 10% Miscelâneas
const BLOCK_ROUNDING = 2;     // Arredondar horas para blocos de 2
const MAX_DAILY_HOURS = 8;    // Teto diário

// FUNÇÃO DE ARREDONDAMENTO DE HORAS
function calculateHours(baseHours) {
    // Regra C: Arredondar para próximo par
    let hours = Math.ceil(baseHours);
    if (hours % 2 !== 0) hours += 1;
    return hours;
}

// FUNÇÃO DE CONTINGÊNCIA (Regra D)
function addContingency(hours) {
    let contingency = Math.ceil(hours * CONTINGENCY_PCT);
    // Mínimo de 2h de contingência se houver trabalho
    if (contingency < 2 && hours > 0) contingency = 2;
    // Arredondar para par
    if (contingency % 2 !== 0) contingency += 1;
    return contingency;
}

// LÓGICA DE PROCESSAMENTO POR ITEM
items.forEach(item => {
    
    // 1. PROCESSAR MATERIAIS (Regra A e E)
    let totalMaterialCost = 0;
    item.hardware.forEach(hw => {
        // BUSCAR NO BANCO DE DADOS (DB_MAT) via 'spec_trigger'
        // Se não achar, marcar como "COTAR"
        // Adicionar ao Array de Materiais do Item
        totalMaterialCost += (hw.cost_net * hw.qty);
    });

    // REGRA E: ADICIONAR MISCELÂNEAS
    if (totalMaterialCost > 0) {
        item.hardware.push({
            description: `Miscelâneas de Instalação e Montagem ${item.item_id}`,
            partnumber: `MISC-${item.item_id}`,
            cost_net: totalMaterialCost * MISC_PCT, // 10%
            qty: 1
        });
    }

    // 2. PROCESSAR MÃO DE OBRA (Regra C e F)
    // Definir Perfis baseados na Complexidade (Low/Med/High)
    // Ex: Se High -> Adicionar Gestor (Regra F)
    
    let roleMap = {
        "Low": { tech: true, aux: false, manager_hrs: 2 },
        "Medium": { tech: true, aux: true, manager_hrs: 8 },
        "High": { tech: true, aux: true, eng: true, manager_hrs: 16 }
    };

    let profile = roleMap[item.labor.complexity_level];
    
    // Adicionar Linhas de MOD
    // Para cada profissional (Técnico, Auxiliar, Eng):
    // - Adicionar Horas Base (Arredondadas)
    // - Adicionar Linha Separada "Contingência Operacional" (Regra D)
    
    // 3. REGRA G: CERTIFICAÇÃO
    if (item.flags.requires_certification) {
        // Adicionar Item Extra no Array Global: "Serviço de Certificação"
        // Adicionar Custo SET (Locação Fluke) do DB_SET
        // Adicionar Logística Reversa (R$ 450,00)
    }
});

// 4. REGRA J: PRECIFICAÇÃO DE VENDA FINAL
// Aplicar Multiplicadores sobre o Custo Final Agregado
// MAT = MAX(List, Net * 2)
// MOD = Net * 3
// SET = Net * 1.6