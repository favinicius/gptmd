## 1. APRESENTAÇÃO INSTITUCIONAL

A **{{COMPANY_NAME}}** é uma integradora de sistemas especializada em automação, elétrica e infraestrutura de TI para ambientes industriais. Nossa missão é entregar soluções robustas que garantam a continuidade operacional.

### AVISO LEGAL E CONFIDENCIALIDADE
Este documento contém informações estritamente confidenciais de propriedade da {{COMPANY_NAME}} e da **{{CLIENT_NAME}}**. Sua reprodução é proibida sem autorização expressa.

---

## 2. ESCOPO TÉCNICO: DATACENTER INDUSTRIAL (IODC)

O objetivo principal deste projeto é estabelecer uma infraestrutura de TI Industrial robusta, observando as melhores práticas do mercado e normas como TIA-942.

### 2.1. Infraestrutura Física e Facilities
O ambiente físico é a base da disponibilidade. Abaixo detalhamos nossa abordagem para energia, climatização e acomodação física.

<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Analise o `scope_json` procurando por itens de infraestrutura física (Racks, Ar Condicionado, Nobreaks/UPS, Cabeamento).
2. Se houver itens: Descreva a solução técnica, mencionando redundância e autonomia de energia se aplicável.
3. Se NÃO houver itens físicos no JSON: Escreva um parágrafo afirmando que "A infraestrutura física (Sala, Energia e Climatização) será provida pelo cliente conforme requisitos do projeto."
4. Seja profissional e direto.
<!-- IA_DYNAMIC_BLOCK_END -->

### 2.2. Hardware de Processamento e Armazenamento
O núcleo computacional do IODC será composto por equipamentos dimensionados para a carga de trabalho industrial.

<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Liste os Servidores e Storage do `scope_json` de forma resumida (ex: "2x Servidores Dell PowerEdge...").
2. Descreva a arquitetura (Cluster, Standalone, Hiperconvergência) inferida pelos itens.
3. Se o hardware for "Client Supplied" (verifique `hardware_supply_by_client` no intent se possível, ou infira do JSON): Deixe claro que a OFI realizará apenas a instalação e configuração.
<!-- IA_DYNAMIC_BLOCK_END -->

### 2.3. Software, Virtualização e Licenciamento

<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Liste o software de base (Windows Server, VMware, SQL) e aplicações industriais.
2. Se não houver licenças no escopo, adicione a nota: "O licenciamento Microsoft e VMware deverá ser disponibilizado pelo cliente, salvo se listado explicitamente abaixo."
<!-- IA_DYNAMIC_BLOCK_END -->

---

## 3. METODOLOGIA DE IMPLANTAÇÃO

Nossa entrega segue o framework **OFI-5D** de qualidade e rastreabilidade:

1.  **Discovery & Plan:** Levantamento detalhado e validação de pré-requisitos.
2.  **Supply & Logistics:** Gestão da cadeia de suprimentos e entrega segura.
3.  **Build (Físico):** Montagem eletromecânica e cabeamento estruturado.
4.  **Deploy (Lógico):** Instalação, hardening e configuração de alta disponibilidade.
5.  **Handover:** Testes assistidos (SAT), documentação As-Built e treinamento.

---

## 4. DETALHAMENTO DE ITENS (BOM)

Abaixo apresentamos a lista consolidada de itens considerados nesta proposta.

<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Gere uma tabela Markdown limpa com as colunas: "Item / Descrição", "Qtd", "Tipo".
2. Agrupe os itens do `scope_json` por afinidade (Hardware, Software, Serviços).
3. Não mostre preços unitários aqui (apenas na proposta comercial).
<!-- IA_DYNAMIC_BLOCK_END -->
