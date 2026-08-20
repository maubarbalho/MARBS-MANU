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


## Atualização do treino guiado

O botão **Iniciar treino guiado** foi reposicionado para ficar imediatamente abaixo do tipo/foco de cada treino. O fluxo agora abre uma janela guiada contextual, em vez de depender apenas do conteúdo do card, com cabeçalho de atividade, exercício em destaque, área para instruções, recorde pessoal, progressão de carga, séries marcáveis, histórico da atividade, navegação entre exercícios e progresso segmentado no rodapé. A mesma composição é alimentada pelos dados dos treinos A, B, C e D.

Durante a validação foi corrigida uma referência antiga ao identificador `guidedProgressLabel`, que havia impedido a primeira renderização do cartão. Após a correção, o layout abriu normalmente, uma série foi acionada e o console permaneceu sem erros JavaScript.


## Atualização do modo guiado — campos por série

O modo de treino guiado foi ajustado para remover a opção de vídeo e aproximar a interação do padrão solicitado: cada linha de série agora possui campos independentes para repetições e peso em quilogramas, além do botão acessível de conclusão. Os valores são normalizados, persistidos em `setDetails` e incorporados ao volume e ao registro de treinos concluídos.

Para preservar a compatibilidade com dados antigos, o aplicativo continua aceitando cargas salvas no campo global por exercício. Durante a migração, uma carga antiga duplicada automaticamente em todas as linhas é mantida apenas como valor inicial da primeira série; as demais ficam editáveis sem duplicação indevida. A opção de vídeo foi removida do cartão guiado, mantendo a navegação, o histórico da atividade, o timer e o progresso da sessão.

A validação visual confirmou o funcionamento no Treino A, incluindo repetições e peso salvos por linha. A validação sintática do JavaScript embutido e do service worker também foi concluída sem erros.


## Atualização — design inspirado no iOS para iPhone

O sistema visual foi adaptado para uma experiência inspirada no padrão nativo do iOS, mantendo o app responsivo e as funcionalidades existentes. Foram aplicados fundo agrupado claro, suporte automático ao modo escuro do sistema, tipografia de sistema, cartões brancos/arredondados, separadores suaves, sombras discretas, azul de ação semelhante ao azul do sistema, botões com estados de toque, barra inferior translúcida com área segura do iPhone e folhas modais com puxador visual.

A navegação inferior deixou de usar emojis coloridos e passou a utilizar símbolos monocromáticos mais discretos. O modo guiado, os campos de repetições e peso por série, o timer e os modais receberam a mesma linguagem visual. Os metadados de instalação foram atualizados para `color-scheme: light dark`, barra de status adaptável, cores de tema claras/escuras e instalação PWA em modo `standalone`.

A versão foi testada no navegador local: a tela inicial, a aba Treinos, o botão de treino guiado, os cartões de séries e a navegação inferior foram carregados sem erros JavaScript no console. O tema acompanha o modo escuro do sistema por meio de `prefers-color-scheme`.
