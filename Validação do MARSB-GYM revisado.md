# Validação do MARSB-GYM revisado

## Testes realizados

- O HTML abriu em servidor local sem falha bloqueante.
- A tela inicial exibiu navegação, semanas, cards de treino, banner de instalação e estatísticas.
- A aba Treinos abriu corretamente.
- O Treino A expandiu e mostrou exercícios, inputs de carga, séries, timer e modo guiado.
- A primeira série foi marcada com sucesso; o contador mudou de 0/21 para 1/21.
- O timer automático abriu e exibiu controles de pausar, pular e adicionar 30 segundos.
- O console exibiu apenas logs do provedor Puter, sem erros JavaScript durante esses fluxos.

## Validações estáticas

- JavaScript embutido extraído e aprovado por `node --check`.
- `sw.js` aprovado por `node --check`.
- `manifest.json` aprovado por parsing JSON.
- Service worker atualizado para cache versionado, navegação network-first e fallback offline.
- A API Key do Coach IA foi migrada para `sessionStorage`; configurações não sensíveis permanecem no `localStorage`.
- Base URL personalizada exige HTTPS, com exceção de localhost para desenvolvimento.
- Carga de exercício foi limitada a 0–1000 kg e normalizada para até duas casas decimais.
- Modo guiado passou a usar conteúdo escapado e listeners programáticos.
- Banner de modo offline e listeners online/offline foram adicionados.
- Bloqueio global de `touchend` foi removido para não prejudicar zoom e acessibilidade.

## Recarga final

A recarga final manteve a inicialização sem erros. A captura visual não mostrou os atalhos na primeira leitura, mas a inspeção do DOM confirmou quatro cards `.qs-card` no container `#quickStart` e a página ativa correta (`page-home`). O console permaneceu sem erros após a recarga.

## Smoke tests do navegador

O service worker foi registrado com escopo na raiz local. A validação aceitou uma Base URL HTTPS, rejeitou HTTP público, aceitou a data atual e rejeitou uma data impossível. Esses testes foram executados diretamente no contexto carregado da aplicação.

## Atualização — novo treino guiado

- O botão `Iniciar treino guiado` foi movido para dentro do cabeçalho de cada card, imediatamente abaixo do tipo/foco do treino.
- Os quatro cards (A, B, C e D) exibem o novo botão no navegador.
- O primeiro smoke test encontrou uma referência antiga a `guidedProgressLabel`, corrigida para `guidedTitle`; após a correção, o cartão passou a renderizar normalmente.
- A nova janela foi verificada visualmente com atividade, exercício, carga atual, recorde pessoal, séries marcáveis, histórico, navegação e progresso segmentado.
- Uma série foi acionada no modo guiado; o estado visual e a persistência foram atualizados sem erros no console.
- O layout é gerado pelo mesmo fluxo para todos os treinos, usando os dados do exercício selecionado.
- O teste visual ocorreu em `http://127.0.0.1:8765/index.html` em 20/08/2026.

- O smoke test final iniciou o Treino D diretamente e confirmou diálogo ativo, título `Exercício 1/9`, identificação `Treino D • Ombros, Bíceps, Tríceps` e quatro séries renderizadas.
- Após a correção, `node --check` aprovou o service worker, o manifesto foi aprovado por parsing JSON e o JavaScript embutido foi extraído sem falha sintática.

## Atualização — peso e repetições por série

- A opção de vídeo foi removida do modo guiado; não há mais controles `.guided-video-btn` ou `.js-guided-video` no diálogo.
- O cartão guiado passou a renderizar campos independentes `guidedReps-*` e `guidedWeight-*` para cada série, além do botão de conclusão acessível.
- O smoke test salvou a primeira série com 8 repetições e 20 kg; a inspeção do `localStorage` confirmou `setDetails.a1[0] = { reps: "8", weight: "20" }` e a carga global sincronizada em 20 kg.
- Após a recarga, os dados antigos que haviam replicado 20 kg em todas as linhas foram migrados para manter 20 kg apenas na primeira série; as linhas seguintes ficaram editáveis sem peso duplicado.
- O JavaScript embutido e o `sw.js` passaram novamente na validação sintática após o último ajuste.

## Atualização — design inspirado no iOS para iPhone

- O tema visual claro foi verificado na tela inicial com fundo agrupado, cartões arredondados, azul de ação, sombras suaves e barra inferior translúcida.
- A navegação inferior foi recarregada com símbolos monocromáticos (`⌂`, `◉`, `＋÷`, `◒`, `✦`, `▥`, `☷`, `ⓘ`) no lugar dos emojis coloridos.
- A aba Treinos abriu normalmente; os quatro cards mantiveram o botão de treino guiado abaixo do tipo/foco do treino.
- O modo guiado abriu com a nova paleta, campos independentes de repetições e peso, histórico, progresso e botões de navegação preservados.
- O console mostrou apenas os logs informativos já existentes do provedor Puter, sem erros JavaScript durante a recarga, navegação e abertura do treino guiado.
- `index.html` passou pela extração e validação do JavaScript embutido; `sw.js` passou por `node --check`; `manifest.json` passou por parsing JSON.
- O manifesto foi atualizado para `theme_color` e `background_color` em `#f2f2f7`, `display_override` em `standalone` e o HTML passou a declarar `color-scheme: light dark`, temas de status bar e cores de tema para os modos claro e escuro.
