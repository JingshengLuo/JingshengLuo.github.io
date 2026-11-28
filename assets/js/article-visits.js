(() => {
  const counter = document.getElementById('article-visits');
  if (!counter) return;

  const { code, path } = counter.dataset;
  if (!/^[a-z0-9][a-z0-9-]*$/.test(code) || !path.startsWith('/')) return;

  const site = `https://${code}.goatcounter.com`;
  const script = document.createElement('script');
  script.dataset.goatcounter = `${site}/count`;
  script.dataset.goatcounterSettings = JSON.stringify({ path });
  script.src = 'https://gc.zgo.at/count.js';
  script.async = true;
  document.head.append(script);

  fetch(`${site}/counter/${encodeURIComponent(path)}.json`, { credentials: 'omit' })
    .then((response) => (response.ok || response.status === 404) ? response.json() : null)
    .then((data) => {
      if (!data || !/^[0-9][0-9,.\s]*$/.test(data.count)) return;

      const label = data.count === '1' ? 'visit' : 'visits';
      counter.textContent = `${data.count} ${label}`;
      counter.hidden = false;
    })
    .catch(() => {
      // The article stays readable if the counter is unavailable.
    });
})();
