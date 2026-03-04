// Criminal Face Generator - Frontend JavaScript

const API_BASE = "/api";
let categories = [];
let selectedFeatures = new Set();
let currentCompositionId = null;
let currentPrompt = "";

// All compositions history (persistent across clears)
let allCompositions = []; // [{id, created_at, versions: [...]}]

// Conversation history for current composition (revision context)
let conversationHistory = []; // array of past revision prompts

// Track which version we're currently working from (for correct parent linking)
let currentActiveVersionId = null;
let currentActiveVersionNumber = null;

// Drawing state
let drawingEnabled = false;
let drawCtx = null;
let drawCanvas = null;
let isDrawing = false;
let brushColor = "#000000";
let brushSize = 3;

// ── INIT ──
document.addEventListener("DOMContentLoaded", () => {
    loadFeatures();
    loadAllHistory();
    setupEventListeners();
    setupDrawing();
});

function getCookie(name) {
    let v = null;
    if (document.cookie && document.cookie !== "") {
        for (const c of document.cookie.split(";")) {
            const t = c.trim();
            if (t.startsWith(name + "=")) {
                v = decodeURIComponent(t.substring(name.length + 1));
                break;
            }
        }
    }
    return v;
}

// ── EVENT LISTENERS ──
function setupEventListeners() {
    document
        .getElementById("generateBtn")
        .addEventListener("click", generateMugshot);
    document
        .getElementById("clearBtn")
        .addEventListener("click", clearSelection);
    document
        .getElementById("copyPromptBtn")
        .addEventListener("click", copyPrompt);
    document
        .getElementById("reviseBtn")
        .addEventListener("click", reviseSketch);
    document
        .getElementById("colorizeBtn")
        .addEventListener("click", colorizeSketch);
    document
        .getElementById("toggleDrawBtn")
        .addEventListener("click", toggleDrawMode);
    document
        .getElementById("clearDrawBtn")
        .addEventListener("click", clearDrawing);
    document.getElementById("brushSize").addEventListener("input", (e) => {
        brushSize = parseInt(e.target.value);
    });

    // User prompt and reference image — update generate button state
    const userPromptEl = document.getElementById("userPrompt");
    if (userPromptEl) {
        userPromptEl.addEventListener("input", () => updateUI());
    }
    const refImageInput = document.getElementById("refImageInput");
    if (refImageInput) {
        refImageInput.addEventListener("change", () => {
            // Show filename preview
            const label = document.getElementById("refImageLabel");
            if (refImageInput.files.length > 0) {
                label.textContent = refImageInput.files[0].name;
                // Show thumbnail preview
                const url = URL.createObjectURL(refImageInput.files[0]);
                document.getElementById("refPreview").src = url;
                document.getElementById("refPreview").style.display = "block";
            } else {
                label.textContent = "Upload Reference Image";
                document.getElementById("refPreview").style.display = "none";
            }
            updateUI();
        });
    }

    // Color buttons
    document.querySelectorAll(".color-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            document
                .querySelectorAll(".color-btn")
                .forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            brushColor = btn.dataset.color;
        });
    });
}

// ── FEATURES ──
async function loadFeatures() {
    try {
        const response = await fetch(`${API_BASE}/categories/`);
        categories = await response.json();
        renderCategories();
    } catch (error) {
        console.error("Error loading features:", error);
        document.getElementById("featuresPanel").innerHTML =
            '<div class="loading-text">Error loading features. Please refresh.</div>';
    }
}

function renderCategories() {
    const panel = document.getElementById("featuresPanel");
    panel.innerHTML = "";

    categories.forEach((category) => {
        const div = document.createElement("div");
        div.className = "category";

        const title = document.createElement("h3");
        title.className = "category-title";
        title.textContent = category.name;
        div.appendChild(title);

        const grid = document.createElement("div");
        grid.className = "features-grid";

        category.features.forEach((feature) => {
            grid.appendChild(createFeatureCard(feature, category.id));
        });

        div.appendChild(grid);
        panel.appendChild(div);
    });
}

function createFeatureCard(feature, categoryId) {
    const card = document.createElement("div");
    card.className = "feature-card";
    card.dataset.featureId = feature.id;
    card.dataset.categoryId = categoryId;

    // Only show image if available
    if (feature.image) {
        const img = document.createElement("img");
        img.src = feature.image;
        img.alt = feature.name;
        card.appendChild(img);
    }

    const name = document.createElement("div");
    name.className = "feature-name";
    name.textContent = feature.name;
    card.appendChild(name);

    card.addEventListener("click", () =>
        toggleFeature(feature, card, categoryId),
    );
    return card;
}

function toggleFeature(feature, card, categoryId) {
    // Radio behavior per category
    document
        .querySelectorAll(`[data-category-id="${categoryId}"]`)
        .forEach((c) => {
            c.classList.remove("selected");
            selectedFeatures.delete(parseInt(c.dataset.featureId));
        });

    card.classList.add("selected");
    selectedFeatures.add(feature.id);

    updateUI();
}

function findFeature(id) {
    for (const cat of categories) {
        const f = cat.features.find((f) => f.id === id);
        if (f) return f;
    }
    return null;
}

function updateUI() {
    const count = selectedFeatures.size;
    const generateBtn = document.getElementById("generateBtn");
    const copyPromptBtn = document.getElementById("copyPromptBtn");
    const userPrompt =
        document.getElementById("userPrompt")?.value.trim() || "";
    const refImageInput = document.getElementById("refImageInput");
    const hasRefImage =
        refImageInput && refImageInput.files && refImageInput.files.length > 0;

    // Enable generate if any input is provided: features, user prompt, or reference image
    const hasInput = count > 0 || userPrompt.length > 0 || hasRefImage;
    generateBtn.disabled = !hasInput;
    copyPromptBtn.disabled = count === 0;

    if (count > 0) {
        updatePromptDisplay();
    } else {
        document.getElementById("promptDisplay").style.display = "none";
        currentPrompt = "";
    }
}

function updatePromptDisplay() {
    const features = Array.from(selectedFeatures)
        .map((id) => {
            const f = findFeature(id);
            return f ? f.prompt_text : "";
        })
        .filter(Boolean)
        .join(", ");

    currentPrompt = `black and white pencil sketch on paper, police sketch artist drawing, Indian person, ${features}, realistic facial features, South Asian features, detailed line art, monochrome criminal identification sketch, harsh lighting, frontal view, mugshot style, NOT idealized or pretty, authentic law enforcement sketch, realistic proportions`;

    const el = document.getElementById("promptDisplay");
    el.textContent = currentPrompt;
    el.style.display = "block";
}

function copyPrompt() {
    if (!currentPrompt) return;
    navigator.clipboard.writeText(currentPrompt).then(() => {
        const btn = document.getElementById("copyPromptBtn");
        const orig = btn.textContent;
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = orig), 2000);
    });
}

// ── STATUS ──
function setStatus(msg, type = "") {
    const bar = document.getElementById("statusBar");
    bar.textContent = msg;
    bar.className = "status-bar visible" + (type ? " " + type : "");
}

function clearStatus() {
    const bar = document.getElementById("statusBar");
    bar.className = "status-bar";
}

// ── IMAGE DISPLAY ──
function showImage(url) {
    const img = document.getElementById("resultImage");
    const placeholder = document.getElementById("placeholder");
    img.src = url;
    img.style.display = "block";
    placeholder.style.display = "none";

    // Show post-generation actions
    document.getElementById("postGenActions").style.display = "flex";
    document.getElementById("revisionArea").style.display = "block";
    document.getElementById("drawToolbar").classList.add("visible");

    // Reset drawing
    disableDrawMode();
    clearDrawing();

    // Resize drawing canvas after image loads
    img.onload = () => {
        resizeDrawingCanvas();
    };
}

function resizeDrawingCanvas() {
    const img = document.getElementById("resultImage");
    drawCanvas = document.getElementById("drawingCanvas");
    drawCanvas.width = img.naturalWidth;
    drawCanvas.height = img.naturalHeight;
    drawCtx = drawCanvas.getContext("2d");
}

// ── DRAWING OVERLAY ──
function setupDrawing() {
    drawCanvas = document.getElementById("drawingCanvas");
    drawCtx = drawCanvas.getContext("2d");

    drawCanvas.addEventListener("mousedown", startDraw);
    drawCanvas.addEventListener("mousemove", draw);
    drawCanvas.addEventListener("mouseup", stopDraw);
    drawCanvas.addEventListener("mouseleave", stopDraw);

    // Touch support
    drawCanvas.addEventListener("touchstart", (e) => {
        e.preventDefault();
        startDraw(touchToMouse(e));
    });
    drawCanvas.addEventListener("touchmove", (e) => {
        e.preventDefault();
        draw(touchToMouse(e));
    });
    drawCanvas.addEventListener("touchend", stopDraw);
}

function touchToMouse(e) {
    const touch = e.touches[0];
    const rect = drawCanvas.getBoundingClientRect();
    return {
        offsetX: (touch.clientX - rect.left) * (drawCanvas.width / rect.width),
        offsetY: (touch.clientY - rect.top) * (drawCanvas.height / rect.height),
    };
}

function toggleDrawMode() {
    if (drawingEnabled) {
        disableDrawMode();
    } else {
        enableDrawMode();
    }
}

function enableDrawMode() {
    drawingEnabled = true;
    drawCanvas.style.display = "block";
    document.getElementById("toggleDrawBtn").textContent = "✓ Drawing ON";
    document.getElementById("toggleDrawBtn").style.background = "#dc3545";
    document.getElementById("toggleDrawBtn").style.color = "#fff";
}

function disableDrawMode() {
    drawingEnabled = false;
    drawCanvas.style.display = "none";
    document.getElementById("toggleDrawBtn").textContent = "✏ Draw";
    document.getElementById("toggleDrawBtn").style.background = "";
    document.getElementById("toggleDrawBtn").style.color = "";
    isDrawing = false;
}

function startDraw(e) {
    if (!drawingEnabled) return;
    isDrawing = true;
    drawCtx.beginPath();
    const { x, y } = getDrawCoords(e);
    drawCtx.moveTo(x, y);
}

function draw(e) {
    if (!isDrawing || !drawingEnabled) return;
    const { x, y } = getDrawCoords(e);
    drawCtx.lineWidth = brushSize;
    drawCtx.lineCap = "round";
    drawCtx.strokeStyle = brushColor;
    drawCtx.lineTo(x, y);
    drawCtx.stroke();
}

function stopDraw() {
    isDrawing = false;
}

function getDrawCoords(e) {
    if (e.offsetX !== undefined) {
        const rect = drawCanvas.getBoundingClientRect();
        return {
            x: e.offsetX * (drawCanvas.width / rect.width),
            y: e.offsetY * (drawCanvas.height / rect.height),
        };
    }
    return { x: e.offsetX, y: e.offsetY };
}

function clearDrawing() {
    if (drawCtx) {
        drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    }
}

function getOverlayBase64() {
    // Check if canvas has any drawing on it
    if (!drawCtx) return null;
    const data = drawCtx.getImageData(
        0,
        0,
        drawCanvas.width,
        drawCanvas.height,
    );
    const hasDrawing = data.data.some((v, i) => i % 4 === 3 && v > 0); // check alpha channel
    if (!hasDrawing) return null;
    return drawCanvas.toDataURL("image/png").split(",")[1];
}

// ── HISTORY SIDEBAR (PERSISTENT & GROUPED) ──
async function loadAllHistory() {
    try {
        const resp = await fetch(`${API_BASE}/compositions/all_history/`);
        allCompositions = await resp.json();
        renderHistory();
    } catch (err) {
        console.error("Error loading all history:", err);
    }
}

function addVersionToCurrentComposition(ver) {
    // Find or create the composition group in allCompositions
    let compGroup = allCompositions.find((c) => c.id === currentCompositionId);
    if (!compGroup) {
        compGroup = {
            id: currentCompositionId,
            created_at: new Date().toISOString(),
            versions: [],
        };
        allCompositions.unshift(compGroup); // newest first
    }
    compGroup.versions.push(ver);
    renderHistory();
}

function renderHistory() {
    const list = document.getElementById("historyList");

    if (allCompositions.length === 0) {
        list.innerHTML = '<div class="history-empty">No generations yet</div>';
        return;
    }

    list.innerHTML = "";

    // Sort newest first
    const sorted = [...allCompositions].sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at),
    );

    sorted.forEach((comp) => {
        const group = document.createElement("div");
        group.className = "history-group";
        if (comp.id === currentCompositionId)
            group.classList.add("active-group");

        // Group header
        const header = document.createElement("div");
        header.className = "hg-header";
        const dt = new Date(comp.created_at);
        header.innerHTML = `
            <span class="hg-id">Composition #${comp.id}</span>
            <span class="hg-date">${dt.toLocaleDateString()} ${dt.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
        `;
        header.addEventListener("click", () => {
            group.classList.toggle("collapsed");
        });
        group.appendChild(header);

        // Version items inside this group
        const versionsList = document.createElement("div");
        versionsList.className = "hg-versions";

        const typeLabels = {
            sketch: "Sketch",
            revision: "Revision",
            colorized: "Colorized",
        };

        // show newest version first within group
        const sortedVersions = [...(comp.versions || [])].reverse();

        sortedVersions.forEach((v) => {
            const item = document.createElement("div");
            item.className = "history-item";
            item.dataset.versionId = v.id;
            item.dataset.compositionId = comp.id;

            item.innerHTML = `
                <div class="hi-version">v${v.version_number}</div>
                <div class="hi-type">${typeLabels[v.image_type] || v.image_type}</div>
                <div class="hi-time">${new Date(v.created_at).toLocaleTimeString()}</div>
                <img class="hi-thumb" src="${v.image}" alt="v${v.version_number}">
            `;

            item.addEventListener("click", (e) => {
                e.stopPropagation();
                restoreVersion(v, comp.id);
            });
            versionsList.appendChild(item);
        });

        group.appendChild(versionsList);
        list.appendChild(group);
    });
}

async function restoreVersion(version, compositionId) {
    const csrftoken = getCookie("csrftoken");
    const targetCompId = compositionId || currentCompositionId;
    setStatus("Restoring version...", "loading");

    try {
        const resp = await fetch(
            `${API_BASE}/compositions/${targetCompId}/restore/${version.id}/`,
            {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
            },
        );

        const result = await resp.json();

        if (result.image_url) {
            // Always update composition context and rebuild conversation
            // history up to the restored version's point in time
            currentCompositionId = targetCompId;
            currentActiveVersionId = version.id;
            currentActiveVersionNumber = version.version_number;

            // Rebuild conversation history: only include revision prompts
            // from versions UP TO the restored version number
            conversationHistory = [];
            const compGroup = allCompositions.find(
                (c) => c.id === targetCompId,
            );
            if (compGroup) {
                compGroup.versions
                    .filter(
                        (v) =>
                            v.version_number <= version.version_number &&
                            v.image_type === "revision" &&
                            v.prompt_used,
                    )
                    .sort((a, b) => a.version_number - b.version_number)
                    .forEach((v) => {
                        conversationHistory.push(v.prompt_used);
                    });
            }
            console.log(
                `[Restore] v${version.version_number}, conversation history: [${conversationHistory.join("; ")}]`,
            );
            showImage(result.image_url);
            // Show post-generation actions since we now have an image
            document.getElementById("postGenActions").style.display = "flex";
            document.getElementById("revisionArea").style.display = "block";
            document.getElementById("drawToolbar").classList.add("visible");

            setStatus(
                `Restored v${version.version_number} (${version.image_type})`,
            );
            setTimeout(clearStatus, 3000);
            renderHistory();
        } else {
            setStatus(result.error || "Restore failed", "error");
        }
    } catch (err) {
        setStatus("Restore error: " + err.message, "error");
    }
}

// ── GENERATE SKETCH ──
async function generateMugshot() {
    const generateBtn = document.getElementById("generateBtn");
    const csrftoken = getCookie("csrftoken");

    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";
    setStatus(
        "Creating composition & generating sketch... (15-30s)",
        "loading",
    );

    try {
        // Gather user prompt and reference image
        const userPrompt =
            document.getElementById("userPrompt")?.value.trim() || "";
        const refImageInput = document.getElementById("refImageInput");
        const refFile =
            refImageInput && refImageInput.files.length > 0
                ? refImageInput.files[0]
                : null;

        // Create composition using FormData (supports file upload)
        const formData = new FormData();
        Array.from(selectedFeatures).forEach((id) => {
            formData.append("selected_features", id);
        });
        if (userPrompt) formData.append("user_prompt", userPrompt);
        if (refFile) formData.append("reference_image", refFile);

        const compResp = await fetch(`${API_BASE}/compositions/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        });

        const composition = await compResp.json();
        currentCompositionId = composition.id;
        conversationHistory = []; // new composition = new conversation
        currentActiveVersionId = null;
        currentActiveVersionNumber = null;

        // Generate sketch
        const sketchResp = await fetch(
            `${API_BASE}/compositions/${composition.id}/generate_sketch/`,
            {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
            },
        );

        const result = await sketchResp.json();

        if (result.image_url) {
            showImage(result.image_url);
            if (result.version) {
                addVersionToCurrentComposition(result.version);
                currentActiveVersionId = result.version.id;
                currentActiveVersionNumber = result.version.version_number;
            }
            setStatus("Sketch generated successfully");
            setTimeout(clearStatus, 3000);
        } else {
            setStatus(result.error || "Generation failed", "error");
        }
    } catch (error) {
        console.error("Error generating mugshot:", error);
        setStatus("Error: " + error.message, "error");
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "Generate Sketch";
    }
}

// ── REVISE SKETCH ──
async function reviseSketch() {
    if (!currentCompositionId) return;

    const prompt = document.getElementById("revisionPrompt").value.trim();
    if (!prompt) {
        setStatus("Please describe the changes you want", "error");
        return;
    }

    const csrftoken = getCookie("csrftoken");
    const overlay = getOverlayBase64();

    setStatus("Revising sketch... (15-30s)", "loading");
    document.getElementById("reviseBtn").disabled = true;

    try {
        const body = { prompt, conversation_history: conversationHistory };
        if (overlay) body.overlay_image = overlay;
        if (currentActiveVersionId)
            body.parent_version_id = currentActiveVersionId;

        const resp = await fetch(
            `${API_BASE}/compositions/${currentCompositionId}/revise_sketch/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(body),
            },
        );

        const result = await resp.json();

        if (result.image_url) {
            showImage(result.image_url);
            document.getElementById("revisionPrompt").value = "";
            conversationHistory.push(prompt); // track for next revision
            if (result.version) {
                addVersionToCurrentComposition(result.version);
                currentActiveVersionId = result.version.id;
                currentActiveVersionNumber = result.version.version_number;
            }
            setStatus("Sketch revised successfully");
            setTimeout(clearStatus, 3000);
        } else {
            setStatus(result.error || "Revision failed", "error");
        }
    } catch (error) {
        console.error("Revision error:", error);
        setStatus("Error: " + error.message, "error");
    } finally {
        document.getElementById("reviseBtn").disabled = false;
    }
}

// ── COLORIZE ──
async function colorizeSketch() {
    if (!currentCompositionId) return;

    const csrftoken = getCookie("csrftoken");
    setStatus("Colorizing sketch... (15-30s)", "loading");
    document.getElementById("colorizeBtn").disabled = true;

    try {
        const resp = await fetch(
            `${API_BASE}/compositions/${currentCompositionId}/colorize/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({}),
            },
        );

        const result = await resp.json();

        if (result.image_url) {
            showImage(result.image_url);
            if (result.version) {
                addVersionToCurrentComposition(result.version);
                currentActiveVersionId = result.version.id;
                currentActiveVersionNumber = result.version.version_number;
            }
            setStatus(
                "Colorized successfully — matching against criminal DB...",
            );
            // Trigger face matching after colorization
            matchCriminals();
        } else {
            setStatus(result.error || "Colorization failed", "error");
        }
    } catch (error) {
        console.error("Colorization error:", error);
        setStatus("Error: " + error.message, "error");
    } finally {
        document.getElementById("colorizeBtn").disabled = false;
    }
}

// ── CRIMINAL DB MATCHING ──
async function matchCriminals() {
    if (!currentCompositionId) return;

    const csrftoken = getCookie("csrftoken");
    const matchSection = document.getElementById("matchSection");
    const matchGrid = document.getElementById("matchGrid");
    matchSection.style.display = "block";
    matchGrid.innerHTML =
        '<div class="match-loading">Scanning criminal database...</div>';

    try {
        const resp = await fetch(
            `${API_BASE}/compositions/${currentCompositionId}/match_criminals/`,
            {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
            },
        );

        const result = await resp.json();

        if (result.matches && result.matches.length > 0) {
            matchGrid.innerHTML = "";
            result.matches.forEach((match, idx) => {
                const card = document.createElement("div");
                card.className = "match-card";
                const pct = (match.similarity * 100).toFixed(1);
                card.innerHTML = `
                    <div class="match-rank">#${idx + 1}</div>
                    <img class="match-img" src="${match.image_url}" alt="${match.criminal_id}">
                    <div class="match-id">${match.criminal_id}</div>
                    <div class="match-score">${pct}%</div>
                `;
                matchGrid.appendChild(card);
            });
            setStatus(`Found ${result.matches.length} potential matches`);
            setTimeout(clearStatus, 5000);
        } else {
            matchGrid.innerHTML =
                '<div class="match-loading">No matches found</div>';
            setStatus("Colorized — no close matches found");
            setTimeout(clearStatus, 3000);
        }
    } catch (err) {
        console.error("Matching error:", err);
        matchGrid.innerHTML =
            '<div class="match-loading">Matching failed</div>';
    }
}

// ── CLEAR ──
function clearSelection() {
    selectedFeatures.clear();
    currentCompositionId = null;
    conversationHistory = [];
    currentActiveVersionId = null;
    currentActiveVersionNumber = null;

    document
        .querySelectorAll(".feature-card")
        .forEach((c) => c.classList.remove("selected"));

    // Reset canvas panel
    document.getElementById("resultImage").style.display = "none";
    document.getElementById("placeholder").style.display = "flex";
    document.getElementById("postGenActions").style.display = "none";
    document.getElementById("revisionArea").style.display = "none";
    document.getElementById("drawToolbar").classList.remove("visible");
    document.getElementById("matchSection").style.display = "none";

    // Reset user prompt and reference image
    const userPromptEl = document.getElementById("userPrompt");
    if (userPromptEl) userPromptEl.value = "";
    const refInput = document.getElementById("refImageInput");
    if (refInput) refInput.value = "";
    const refLabel = document.getElementById("refImageLabel");
    if (refLabel) refLabel.textContent = "Upload Reference Image";
    const refPreview = document.getElementById("refPreview");
    if (refPreview) refPreview.style.display = "none";

    // Re-render history to remove active-group highlight (but keep all history)
    renderHistory();

    disableDrawMode();
    clearDrawing();
    clearStatus();
    updateUI();
}

function downloadImage(url) {
    const a = document.createElement("a");
    a.href = url;
    a.download = `criminal_face_${Date.now()}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

