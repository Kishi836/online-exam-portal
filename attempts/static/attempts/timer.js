(() => {
  const timer = document.getElementById("timer");
  if (!timer) {
    return;
  }

  let remaining = Number(timer.dataset.remaining || 0);
  let lastTick = performance.now();

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainder = seconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`;
  };

  const render = () => {
    timer.textContent = remaining > 0 ? formatTime(remaining) : "Time is up";
  };

  const tick = () => {
    const now = performance.now();
    const elapsedSeconds = Math.floor((now - lastTick) / 1000);
    if (elapsedSeconds > 0) {
      remaining = Math.max(0, remaining - elapsedSeconds);
      lastTick += elapsedSeconds * 1000;
      render();
    }
  };

  const resync = async () => {
    if (!timer.dataset.remainingUrl) {
      return;
    }
    try {
      const response = await fetch(timer.dataset.remainingUrl, { credentials: "same-origin" });
      if (!response.ok) {
        return;
      }
      const payload = await response.json();
      remaining = Math.max(0, Number(payload.remaining_seconds) || 0);
      lastTick = performance.now();
      render();
    } catch (_) {}
  };

  render();
  window.setInterval(tick, 250);
  window.setInterval(resync, 60000);
})();
