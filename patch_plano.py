from pathlib import Path

path = Path('/home/ubuntu/upload/index.html')
s = path.read_text()

old = '''      exercises.forEach(function (ex, idx) {
        html += '<div class="menu-item" style="border:1px solid var(--border);border-radius:10px;padding:10px;margin-bottom:6px;background:var(--bg);">' +
          '<div style="flex:1;">' +
            '<div class="menu-item-name">' + (idx + 1) + '. ' + ex.nome + '</div>' +
            '<div class="menu-item-sub">' + ex.series + ' séries · ' + ex.reps + ' reps · ' + ex.descanso + 's' +
            (ex.tech ? ' · ' + ex.tech : '') + '</div>' +
          '</div>' +
          '<button type="button" class="btn-action danger" style="padding:6px 10px;min-width:auto;font-size:0.75rem;" ' +
            'onclick="planoRemoveExercise(' + idx + ')">Remover</button>' +
        '</div>';
      });
      list.innerHTML = html;
'''
new = '''      exercises.forEach(function (ex, idx) {
        var item = document.createElement('div');
        item.className = 'menu-item';
        item.style.cssText = 'border:1px solid var(--border);border-radius:10px;padding:10px;margin-bottom:6px;background:var(--bg);';
        item.innerHTML = '<div style="flex:1;">' +
            '<div class="menu-item-name"></div>' +
            '<div class="menu-item-sub"></div>' +
          '</div>' +
          '<button type="button" class="btn-action danger js-remove-ex" style="padding:6px 10px;min-width:auto;font-size:0.75rem;">Remover</button>';
        
        item.querySelector('.menu-item-name').textContent = (idx + 1) + '. ' + ex.nome;
        item.querySelector('.menu-item-sub').textContent = ex.series + ' séries · ' + ex.reps + ' reps · ' + ex.descanso + 's' + (ex.tech ? ' · ' + ex.tech : '');
        item.querySelector('.js-remove-ex').addEventListener('click', function() { planoRemoveExercise(idx); });
        list.appendChild(item);
      });
'''
assert old in s
s = s.replace(old, new, 1)

old = '''      list.innerHTML = hist.map(h => {
        const weightsStr = Object.entries(h.weights || {})
          .filter(([,v]) => v)
          .map(([exId, w]) => {
            const ex = findExercise(exId);
            return ex ? `${ex.nome}: ${w}kg` : `${exId}: ${w}kg`;
          })
          .join('<br>');

        return `
          <div class="history-item">
            <div class="hi-date">${formatDate(h.date)} • Semana ${h.week}</div>
            <div class="hi-treino">Treino ${h.treino} — ${treinosMap()[h.treino]?.nome || ''}</div>
            ${weightsStr ? `<div class="hi-weights">${weightsStr}</div>` : ''}
            <div class="hi-actions">
              <button class="hi-del" onclick="deleteHistoryEntry('${h.id}')">Apagar registro</button>
            </div>
          </div>
        `;
      }).join('');
'''
new = '''      hist.forEach(h => {
        const item = document.createElement('div');
        item.className = 'history-item';
        
        const weightsStr = Object.entries(h.weights || {})
          .filter(([,v]) => v)
          .map(([exId, w]) => {
            const ex = findExercise(exId);
            const name = ex ? ex.nome : exId;
            return escapeHtml(name) + ': ' + escapeHtml(w) + 'kg';
          })
          .join('<br>');

        const treinoNome = treinosMap()[h.treino]?.nome || '';
        
        item.innerHTML = `
          <div class="hi-date">${escapeHtml(formatDate(h.date))} • Semana ${escapeHtml(h.week)}</div>
          <div class="hi-treino">Treino ${escapeHtml(h.treino)} — ${escapeHtml(treinoNome)}</div>
          ${weightsStr ? `<div class="hi-weights">${weightsStr}</div>` : ''}
          <div class="hi-actions">
            <button class="hi-del js-del-hist" type="button">Apagar registro</button>
          </div>
        `;
        item.querySelector('.js-del-hist').addEventListener('click', () => deleteHistoryEntry(h.id));
        list.appendChild(item);
      });
'''
assert old in s
s = s.replace(old, new, 1)

path.write_text(s)
print('patched plano', path)
