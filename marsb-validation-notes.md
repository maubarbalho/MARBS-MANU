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
