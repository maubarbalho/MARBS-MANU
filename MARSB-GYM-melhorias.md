# MARSB-GYM — versão revisada

## Resultado

O código do MARSB-GYM foi revisado e melhorado sem remover as funcionalidades existentes. A versão atual está mais próxima de um **8,8/10 como MVP local/PWA**, com ganhos importantes em segurança de entrada, estabilidade, acessibilidade, privacidade e experiência mobile.

A avaliação considera que o aplicativo continua sendo um front-end estático, com dados armazenados no navegador. Para chegar a um nível de produto profissional distribuído para muitos usuários, ainda seria recomendável adicionar backend, autenticação, sincronização entre dispositivos e uma política formal de privacidade.

## Arquivos entregues

| Arquivo | Finalidade |
|---|---|
| `index.html` | Interface, lógica do app, validações, acessibilidade e Coach IA revisados. |
| `manifest.json` | Manifesto PWA com identidade, idioma, escopo e ícones instaláveis. |
| `sw.js` | Service worker com cache versionado, atualização e fallback offline. |
| `icon-192.png` e `icon-512.png` | Ícones originais preservados. |

## Principais melhorias

| Área | Alteração realizada | Benefício |
|---|---|---|
| Segurança de entrada | Conteúdo de exercícios, notas, histórico, pesos e dados importados passou a ser escapado antes da renderização. | Reduz risco de injeção de HTML/script por personalizações ou backups. |
| Coach IA | API Key personalizada deixou de ser mantida no `localStorage` e passou para `sessionStorage`; configurações não secretas permanecem no armazenamento persistente. | A chave é removida ao encerrar a sessão do navegador e não entra no backup comum. |
| Coach IA | Base URL personalizada exige HTTPS, com exceção de localhost; modelo e prompt recebem limites de tamanho; requisições têm timeout de 30 segundos. | Evita endpoints inseguros e requisições indefinidamente pendentes. |
| Privacidade | O modal informa que contexto do atleta e conversas podem ser enviados ao provedor escolhido. | Melhora transparência antes do uso de IA externa. |
| Dados de treino | Cargas são normalizadas para até duas casas decimais e limitadas entre 0 e 1000 kg. | Evita valores inválidos e históricos inconsistentes. |
| Peso corporal | Registros aceitam somente datas ISO válidas até o dia atual e pesos entre 30 e 300 kg. | Evita datas impossíveis, registros futuros e dados pessoais inválidos. |
| Histórico | A lista é limpa antes de cada renderização. | Evita duplicação de registros ao atualizar ou apagar dados. |
| Modo guiado | O conteúdo dinâmico usa escape e listeners programáticos, sem handlers inline para séries, timer e navegação. | Melhora segurança, manutenção e previsibilidade dos eventos. |
| Acessibilidade | Foram preservados/fortalecidos foco visível, zoom, navegação por teclado, `aria-expanded`, `aria-controls`, rótulos associados e nomes acessíveis. | Facilita uso por teclado, leitores de tela e usuários de celular. |
| Mobile | O bloqueio global de toque duplo foi removido. | Evita interferência em zoom, gestos e teclado virtual. |
| Offline | Foi adicionado aviso explícito de modo offline. | Deixa claro que treinos, histórico e calculadoras continuam disponíveis, mas o Coach IA exige conexão. |
| PWA | Manifesto com `id`, idioma, escopo, orientação, categorias e ícones `maskable`; service worker com cache versionado e estratégias network-first/stale-while-revalidate. | Melhora instalação, atualização e tolerância a falhas de rede. |

## Validação

A checagem sintática do JavaScript embutido foi concluída com sucesso após a extração para um arquivo independente. O `sw.js` também passou na checagem sintática, e o `manifest.json` foi validado como JSON. Os arquivos essenciais e os dois ícones estão presentes no diretório final.

Também foi realizado um smoke test no navegador em servidor local. A tela inicial carregou, a aba de treinos abriu, o Treino A foi expandido, uma série foi marcada e o timer automático foi acionado. O contador mudou de `0/21` para `1/21`, e não foram observados erros JavaScript no console durante esses fluxos. O service worker foi registrado com escopo na raiz local.

As validações adicionais confirmaram que uma Base URL HTTPS é aceita, que HTTP público é rejeitado, que a data atual é aceita e que uma data impossível como `2026-02-31` é rejeitada.

## Backup

Antes das alterações foi criada uma cópia dos arquivos originais em `marsb-gym-original/`, incluindo o arquivo `SHA256SUMS.txt`. Essa cópia não é utilizada pelo app e serve apenas para restauração ou comparação.

## Observação importante sobre a API própria

Mesmo armazenada somente em `sessionStorage`, uma API Key usada diretamente no navegador **não é um segredo absoluto**: qualquer script executado na mesma origem pode, em princípio, acessar a sessão. Para publicação aberta, a arquitetura recomendada é mover as chamadas aos provedores de IA para um backend ou função server-side, mantendo a chave fora do navegador.

## Como usar

Extraia o pacote e publique o conteúdo de `marsb-gym-melhorado/` em um servidor HTTPS. O service worker não funciona corretamente em `file://`; para testar localmente, use um servidor HTTP local. Depois de atualizar a aplicação publicada, o service worker fará a troca para a nova versão após a instalação e ativação do cache.

