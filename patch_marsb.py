from pathlib import Path

path = Path('/home/ubuntu/upload/index.html')
s = path.read_text()

old = '''    function saveState() {
      localStorage.setItem('marsbGym_v2', JSON.stringify(state));
    }
'''
new = '''    const STORAGE_KEY = 'marsbGym_v2';

    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>'\"]/g, (char) => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '\"': '&quot;'
      }[char]));
    }

    function encodeData(value) {
      return encodeURIComponent(String(value ?? ''));
    }

    function decodeData(value) {
      try { return decodeURIComponent(value || ''); } catch (e) { return ''; }
    }

    function saveState() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      } catch (e) {
        showToast('Não foi possível salvar neste dispositivo. Exporte um backup.');
      }
    }
'''
assert old in s
s = s.replace(old, new, 1)
s = s.replace("localStorage.getItem('marsbGym_v2')", "localStorage.getItem(STORAGE_KEY)", 1)

old = '''        el.className = 'qs-card';
        el.onclick = () => openTreino(t.id);
        el.innerHTML = `
          ${done ? '<span class="qs-done">✓ Feito</span>' : ''}
          <div class="qs-letter qs-${t.id.toLowerCase()}">${t.id}</div>
          <div class="qs-name">${t.nome.split('+')[0].trim()}</div>
        `;
        container.appendChild(el);
'''
new = '''        el.className = 'qs-card';
        el.setAttribute('role', 'button');
        el.setAttribute('tabindex', '0');
        el.setAttribute('aria-label', `Abrir Treino ${t.id}: ${t.nome.split('+')[0].trim()}`);
        const open = () => openTreino(t.id);
        el.addEventListener('click', open);
        el.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); }
        });
        el.innerHTML = `
          ${done ? '<span class="qs-done">✓ Feito</span>' : ''}
          <div class="qs-letter qs-${escapeHtml(t.id.toLowerCase())}">${escapeHtml(t.id)}</div>
          <div class="qs-name">${escapeHtml(t.nome.split('+')[0].trim())}</div>
        `;
        container.appendChild(el);
'''
assert old in s
s = s.replace(old, new, 1)

old = '''        card.innerHTML = `
          <div class="card-header" onclick="toggleCard('${treino.id}')">
            <div>
              <div class="card-title">
                <span class="badge badge-${treino.color}">Treino ${treino.id}</span>
                ${treino.nome}
                ${complete ? ' <span style="color:var(--accent);font-size:0.8rem;">✓</span>' : ''}
              </div>
              <div class="card-meta">${doneSets}/${totalSets} séries • ${treino.foco}</div>
            </div>
            <span class="chevron">▼</span>
          </div>
          <div class="card-body" id="body-${treino.id}"></div>
        `;
        container.appendChild(card);

        const body = card.querySelector('.card-body');
'''
new = '''        card.innerHTML = `
          <div class="card-header js-card-toggle" role="button" tabindex="0" aria-expanded="false" aria-controls="body-${encodeData(treino.id)}">
            <div>
              <div class="card-title">
                <span class="badge badge-${escapeHtml(treino.color)}">Treino ${escapeHtml(treino.id)}</span>
                ${escapeHtml(treino.nome)}
                ${complete ? ' <span style="color:var(--accent);font-size:0.8rem;">✓</span>' : ''}
              </div>
              <div class="card-meta">${doneSets}/${totalSets} séries • ${escapeHtml(treino.foco)}</div>
            </div>
            <span class="chevron" aria-hidden="true">▼</span>
          </div>
          <div class="card-body" id="body-${encodeData(treino.id)}"></div>
        `;
        container.appendChild(card);

        const header = card.querySelector('.js-card-toggle');
        const toggle = () => {
          toggleCard(treino.id);
          header.setAttribute('aria-expanded', card.classList.contains('open') ? 'true' : 'false');
        };
        header.addEventListener('click', toggle);
        header.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); toggle(); }
        });

        const body = card.querySelector('.card-body');
'''
assert old in s
s = s.replace(old, new, 1)

old = '''          const lastTimeHtml = (lastEntry && lastEntry.week !== currentWeek)
            ? `<div class="last-time-hint">🕓 Última vez (Semana ${lastEntry.week}): <strong>${lastEntry.weight}kg</strong></div>`
            : '';

          const histHtml = hist.length
            ? `<div class="weight-history">Histórico: ${hist.map(h => `<span>${h.weight}kg</span> (S${h.week})`).join(' → ')}</div>`
            : '';
'''
new = '''          const lastTimeHtml = (lastEntry && lastEntry.week !== currentWeek)
            ? `<div class="last-time-hint">🕓 Última vez (Semana ${escapeHtml(lastEntry.week)}): <strong>${escapeHtml(lastEntry.weight)}kg</strong></div>`
            : '';

          const histHtml = hist.length
            ? `<div class="weight-history">Histórico: ${hist.map(h => `<span>${escapeHtml(h.weight)}kg</span> (S${escapeHtml(h.week)})`).join(' → ')}</div>`
            : '';
'''
assert old in s
s = s.replace(old, new, 1)

old = '''          exEl.innerHTML = `
            <div class="exercise-top">
              <div class="exercise-name">${ex.nome}</div>
              <div class="exercise-icons">
                <button class="exercise-icon-btn" onclick="openEditExercise('${ex.id}', '${treino.id}')" title="Editar">✏️</button>
              </div>
            </div>
            <div class="exercise-details">
              <span>📊 ${ex.series} × ${ex.reps}</span>
              <span>⏱ ${formatRest(ex.descanso)}</span>
              ${ex.isCustom ? '<span class="badge badge-purple">Personalizado</span>' : ''}
            </div>
            <div class="tech-note">${ex.tech}</div>
            ${(state.exerciseNotes && state.exerciseNotes[ex.id]) ? `<div class="tech-note" style="border-left:3px solid var(--cyan);">📝 ${state.exerciseNotes[ex.id]}</div>` : ''}
            ${lastTimeHtml}
            <div class="weight-row">
              <label>Peso:</label>
              <input type="number" class="weight-input" inputmode="decimal" placeholder="${lastEntry ? lastEntry.weight : '0'}" value="${weight}"
                     onchange="saveWeight('${ex.id}', this.value)" onblur="saveWeight('${ex.id}', this.value)" />
              <span class="weight-unit">kg</span>
            </div>
            ${hist.length ? `
            <div class="weight-history-row">
              ${histHtml}
              <button class="chart-link-btn" onclick="openChart('${ex.id}')">📈 Gráfico</button>
            </div>` : ''}
            <div class="sets-row">
              ${Array.from({length: ex.series}, (_, i) => `
                <button class="set-btn ${doneArr[i] ? 'done' : ''}"
                        onclick="toggleSet('${ex.id}', ${i}, ${ex.descanso}, '${treino.id}')">${i+1}</button>
              `).join('')}
              <button class="rest-btn" onclick="startTimer(${ex.descanso})">⏱ Timer</button>
            </div>
          `;
          body.appendChild(exEl);
'''
new = '''          exEl.innerHTML = `
            <div class="exercise-top">
              <div class="exercise-name">${escapeHtml(ex.nome)}</div>
              <div class="exercise-icons">
                <button class="exercise-icon-btn js-edit-exercise" type="button" title="Editar exercício" aria-label="Editar ${escapeHtml(ex.nome)}">✏️</button>
              </div>
            </div>
            <div class="exercise-details">
              <span>📊 ${escapeHtml(ex.series)} × ${escapeHtml(ex.reps)}</span>
              <span>⏱ ${escapeHtml(formatRest(ex.descanso))}</span>
              ${ex.isCustom ? '<span class="badge badge-purple">Personalizado</span>' : ''}
            </div>
            <div class="tech-note">${escapeHtml(ex.tech)}</div>
            ${(state.exerciseNotes && state.exerciseNotes[ex.id]) ? `<div class="tech-note" style="border-left:3px solid var(--cyan);">📝 ${escapeHtml(state.exerciseNotes[ex.id])}</div>` : ''}
            ${lastTimeHtml}
            <div class="weight-row">
              <label for="weight-${encodeData(ex.id)}">Peso:</label>
              <input type="number" id="weight-${encodeData(ex.id)}" class="weight-input js-save-weight" inputmode="decimal" placeholder="${escapeHtml(lastEntry ? lastEntry.weight : '0')}" value="${escapeHtml(weight)}" min="0" max="1000" step="0.1" />
              <span class="weight-unit">kg</span>
            </div>
            ${hist.length ? `
            <div class="weight-history-row">
              ${histHtml}
              <button class="chart-link-btn js-open-chart" type="button">📈 Gráfico</button>
            </div>` : ''}
            <div class="sets-row">
              ${Array.from({length: ex.series}, (_, i) => `
                <button class="set-btn js-toggle-set ${doneArr[i] ? 'done' : ''}" type="button" data-set-index="${i}">${i+1}</button>
              `).join('')}
              <button class="rest-btn js-start-rest" type="button">⏱ Timer</button>
            </div>
          `;
          exEl.querySelector('.js-edit-exercise').addEventListener('click', () => openEditExercise(ex.id, treino.id));
          exEl.querySelector('.js-save-weight').addEventListener('change', (event) => saveWeight(ex.id, event.currentTarget.value));
          exEl.querySelector('.js-save-weight').addEventListener('blur', (event) => saveWeight(ex.id, event.currentTarget.value));
          exEl.querySelector('.js-open-chart')?.addEventListener('click', () => openChart(ex.id));
          exEl.querySelectorAll('.js-toggle-set').forEach((button) => {
            button.addEventListener('click', () => toggleSet(ex.id, Number(button.dataset.setIndex), ex.descanso, treino.id));
          });
          exEl.querySelector('.js-start-rest').addEventListener('click', () => startTimer(ex.descanso));
          body.appendChild(exEl);
'''
assert old in s
s = s.replace(old, new, 1)

old = '''          actionsRow.innerHTML = `<button class="guided-start-btn" onclick="startGuided('${treino.id}')">▶ Iniciar treino guiado</button>`;
          body.appendChild(actionsRow);
'''
new = '''          actionsRow.innerHTML = '<button class="guided-start-btn" type="button">▶ Iniciar treino guiado</button>';
          actionsRow.querySelector('button').addEventListener('click', () => startGuided(treino.id));
          body.appendChild(actionsRow);
'''
assert old in s
s = s.replace(old, new, 1)

path.write_text(s)
print('patched', path)
