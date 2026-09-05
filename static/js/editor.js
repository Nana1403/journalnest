(function () {
  "use strict";

  var data = document.getElementById("editor-data");
  var titleEl = document.getElementById("note-title");
  var bodyEl = document.getElementById("note-body");
  var statusEl = document.getElementById("save-status");
  var saveBtn = document.getElementById("save-btn");
  var banner = document.getElementById("conflict-banner");
  var reloadBtn = document.getElementById("conflict-reload");
  var keepBtn = document.getElementById("conflict-keep");

  if (!data || !titleEl || !bodyEl) {
    return;
  }

  var autosaveUrl = data.dataset.autosaveUrl;
  var revision = parseInt(data.dataset.revision, 10) || 0;
  var dirty = false;
  var timer = null;
  var inFlight = false;
  var conflictServer = null;
  var DEBOUNCE_MS = 1200;

  function getCookie(name) {
    var match = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return match ? decodeURIComponent(match.pop()) : "";
  }

  function setStatus(state, text) {
    statusEl.dataset.state = state;
    statusEl.textContent = text;
  }

  function autoGrow() {
    bodyEl.style.height = "auto";
    bodyEl.style.height = bodyEl.scrollHeight + "px";
  }

  function markDirty() {
    dirty = true;
    if (statusEl.dataset.state !== "error") {
      setStatus("unsaved", "Unsaved");
    }
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(save, DEBOUNCE_MS);
  }

  function save() {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
    if (inFlight || !dirty) {
      return;
    }
    inFlight = true;
    setStatus("saving", "Saving…");

    fetch(autosaveUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
        "X-Requested-With": "XMLHttpRequest"
      },
      body: JSON.stringify({
        title: titleEl.value,
        content: bodyEl.value,
        revision: revision
      })
    })
      .then(function (resp) {
        return resp.json().then(function (payload) {
          return { status: resp.status, payload: payload };
        });
      })
      .then(function (result) {
        inFlight = false;
        if (result.status === 200) {
          revision = result.payload.revision;
          dirty = false;
          banner.hidden = true;
          setStatus("saved", "Saved " + formatTime(result.payload.saved_at));
        } else if (result.status === 409) {
          conflictServer = result.payload.server;
          setStatus("error", "Could not save — changed elsewhere");
          banner.hidden = false;
        } else {
          setStatus("error", "Could not save — will retry");
          scheduleRetry();
        }
      })
      .catch(function () {
        inFlight = false;
        setStatus("error", "Could not save — will retry");
        scheduleRetry();
      });
  }

  function scheduleRetry() {
    if (timer) {
      clearTimeout(timer);
    }
    // Keep the typed text; try again after a short pause.
    timer = setTimeout(save, 4000);
  }

  function formatTime(iso) {
    try {
      var d = new Date(iso);
      return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    } catch (e) {
      return "";
    }
  }

  titleEl.addEventListener("input", markDirty);
  bodyEl.addEventListener("input", function () {
    autoGrow();
    markDirty();
  });

  if (saveBtn) {
    saveBtn.addEventListener("click", function () {
      if (!dirty) {
        setStatus("saved", "Saved");
        return;
      }
      save();
    });
  }

  if (reloadBtn) {
    reloadBtn.addEventListener("click", function () {
      if (!conflictServer) {
        return;
      }
      titleEl.value = conflictServer.title;
      bodyEl.value = conflictServer.content;
      revision = conflictServer.revision;
      dirty = false;
      banner.hidden = true;
      autoGrow();
      setStatus("saved", "Loaded latest version");
    });
  }

  if (keepBtn) {
    keepBtn.addEventListener("click", function () {
      if (!conflictServer) {
        return;
      }
      // Adopt the server revision so the next save applies on top of it,
      // but keep the text the user typed.
      revision = conflictServer.revision;
      banner.hidden = true;
      dirty = true;
      setStatus("unsaved", "Unsaved");
    });
  }

  window.addEventListener("beforeunload", function (event) {
    if (dirty) {
      event.preventDefault();
      event.returnValue = "";
    }
  });

  autoGrow();
})();
