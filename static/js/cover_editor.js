(function () {
  "use strict";

  // Live client-side preview of the notebook cover on the create form.
  var form = document.getElementById("notebook-form");
  var preview = document.getElementById("cover-preview");
  var previewLabel = document.getElementById("cover-preview-label");
  var previewType = document.getElementById("cover-preview-type");
  
  // Exit early if essential elements are missing
  if (!form || !preview) {
    console.warn("Required elements not found: form or preview");
    return;
  }

  var COLORS = ["cream", "blush", "sage", "lavender", "sky", "burgundy"];
  var PATTERNS = ["plain", "dots", "stripes", "grid", "floral"];
  var FONTS = ["caveat", "patrick_hand", "shadows", "gaegu"];

  function field(name) {
    // Try to find checked radio/checkbox first
    var checked = form.querySelector("[name=" + name + "]:checked");
    if (checked) return checked;
    
    // Fallback to first matching element
    return form.querySelector("[name=" + name + "]");
  }

  function getFieldValue(name, defaultValue) {
    var el = field(name);
    return el ? el.value : defaultValue;
  }

  function render() {
    try {
      var labelInput = form.querySelector("[name=label]");
      
      // Get values with defaults
      var color = getFieldValue("cover_color", "cream");
      var pattern = getFieldValue("cover_pattern", "plain");
      var font = getFieldValue("label_font", "caveat");
      
      // Get notebook type label
      var typeInput = field("notebook_type");
      var typeLabel = "Blank";
      
      if (typeInput) {
        var chosen = form.querySelector(
          "[name=notebook_type][value='" + typeInput.value + "']"
        );
        if (chosen) {
          var wrap = chosen.closest("label");
          typeLabel = wrap ? wrap.textContent.trim() : typeInput.value;
        } else {
          typeLabel = typeInput.value || "Blank";
        }
      }

      // Update color classes
      COLORS.forEach(function (c) { 
        preview.classList.remove("cover--" + c); 
      });
      preview.classList.add("cover--" + color);

      // Update pattern classes
      PATTERNS.forEach(function (p) { 
        preview.classList.remove("cover--pattern-" + p); 
      });
      preview.classList.add("cover--pattern-" + pattern);

      // Update font classes
      FONTS.forEach(function (f) { 
        previewLabel.classList.remove("font-" + f); 
      });
      previewLabel.classList.add("font-" + font);

      // Update label text
      previewLabel.textContent = (labelInput && labelInput.value) 
        ? labelInput.value 
        : "Your label";
      
      // Update type text
      previewType.textContent = typeLabel;
      
    } catch (error) {
      console.error("Error rendering preview:", error);
    }
  }

  form.addEventListener("input", render);
  form.addEventListener("change", render);
  
  // Initial render
  render();
})();