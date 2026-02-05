// Criminal Face Generator - Frontend JavaScript

const API_BASE = "/api";
let categories = [];
let selectedFeatures = new Set();
let currentCompositionId = null;
let currentPrompt = "";
let canvas, ctx;

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
    canvas = document.getElementById("compositeCanvas");
    ctx = canvas.getContext("2d");

    initializeCanvas();
    loadFeatures();
    setupEventListeners();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1),
                );
                break;
            }
        }
    }
    return cookieValue;
}

function initializeCanvas() {
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Add placeholder text
    ctx.fillStyle = "#cccccc";
    ctx.font = "16px Arial";
    ctx.textAlign = "center";
    ctx.fillText(
        "Select features to begin",
        canvas.width / 2,
        canvas.height / 2,
    );
}

function setupEventListeners() {
    document
        .getElementById("generateBtn")
        .addEventListener("click", generateMugshot);
    document
        .getElementById("copyPromptBtn")
        .addEventListener("click", copyPrompt);
    document
        .getElementById("clearBtn")
        .addEventListener("click", clearSelection);
}

async function loadFeatures() {
    try {
        const response = await fetch(`${API_BASE}/categories/`);
        categories = await response.json();
        renderCategories();
    } catch (error) {
        console.error("Error loading features:", error);
        document.getElementById("featuresPanel").innerHTML =
            '<div class="loading">Error loading features. Please refresh.</div>';
    }
}

function renderCategories() {
    const panel = document.getElementById("featuresPanel");
    panel.innerHTML = "";

    categories.forEach((category) => {
        const categoryDiv = document.createElement("div");
        categoryDiv.className = "category";

        const title = document.createElement("h3");
        title.className = "category-title";
        title.textContent = category.name;
        categoryDiv.appendChild(title);

        const grid = document.createElement("div");
        grid.className = "features-grid";

        category.features.forEach((feature) => {
            const card = createFeatureCard(feature, category.id);
            grid.appendChild(card);
        });

        categoryDiv.appendChild(grid);
        panel.appendChild(categoryDiv);
    });
}

function createFeatureCard(feature, categoryId) {
    const card = document.createElement("div");
    card.className = "feature-card";
    card.dataset.featureId = feature.id;
    card.dataset.categoryId = categoryId;

    const imageDiv = document.createElement("div");
    imageDiv.className = "feature-image";

    if (feature.image) {
        const img = document.createElement("img");
        img.src = feature.image;
        img.alt = feature.name;
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "cover";
        imageDiv.appendChild(img);
    } else {
        imageDiv.textContent = "No image";
    }

    const name = document.createElement("div");
    name.className = "feature-name";
    name.textContent = feature.name;

    card.appendChild(imageDiv);
    card.appendChild(name);

    card.addEventListener("click", () =>
        toggleFeature(feature, card, categoryId),
    );

    return card;
}

function toggleFeature(feature, card, categoryId) {
    // Remove other selections from the same category (radio behavior)
    document
        .querySelectorAll(`[data-category-id="${categoryId}"]`)
        .forEach((c) => {
            c.classList.remove("selected");
            const featureId = parseInt(c.dataset.featureId);
            selectedFeatures.delete(featureId);
        });

    // Add current selection
    card.classList.add("selected");
    selectedFeatures.add(feature.id);

    updateCanvas();
    updateSelectedCount();
}

function updateCanvas() {
    // Clear canvas
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (selectedFeatures.size === 0) {
        ctx.fillStyle = "#cccccc";
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.fillText(
            "Select features to begin",
            canvas.width / 2,
            canvas.height / 2,
        );
        return;
    }

    // Draw selected features as text labels (will be enhanced with actual images)
    ctx.fillStyle = "#333333";
    ctx.font = "14px Arial";
    ctx.textAlign = "left";

    let yPos = 30;
    selectedFeatures.forEach((featureId) => {
        const feature = findFeature(featureId);
        if (feature) {
            ctx.fillText(`✓ ${feature.name}`, 20, yPos);
            yPos += 25;
        }
    });

    // Add instruction
    if (selectedFeatures.size > 0) {
        ctx.fillStyle = "#dc3545";
        ctx.font = "bold 14px Arial";
        ctx.textAlign = "center";
        ctx.fillText(
            'Click "Generate Mugshot" to create face',
            canvas.width / 2,
            canvas.height - 30,
        );
    }
}

function findFeature(featureId) {
    for (const category of categories) {
        const feature = category.features.find((f) => f.id === featureId);
        if (feature) return feature;
    }
    return null;
}

function updateSelectedCount() {
    const count = selectedFeatures.size;
    const countEl = document.getElementById("selectedCount");
    const generateBtn = document.getElementById("generateBtn");
    const copyPromptBtn = document.getElementById("copyPromptBtn");

    if (count === 0) {
        countEl.textContent = "No features selected";
        generateBtn.disabled = true;
        copyPromptBtn.disabled = true;
        currentPrompt = "";
        document.getElementById("promptDisplay").style.display = "none";
    } else {
        countEl.textContent = `${count} feature${count > 1 ? "s" : ""} selected`;
        generateBtn.disabled = false;
        copyPromptBtn.disabled = false;
        updatePromptDisplay();
    }
}

function updatePromptDisplay() {
    const features = Array.from(selectedFeatures)
        .map((id) => {
            const feature = findFeature(id);
            return feature ? feature.prompt_text : "";
        })
        .filter((text) => text)
        .join(", ");

    currentPrompt = `black and white pencil sketch on paper, police sketch artist drawing, Indian person, ${features}, realistic facial features, South Asian features, detailed line art, monochrome criminal identification sketch, harsh lighting, frontal view, mugshot style, NOT idealized or pretty, authentic law enforcement sketch, realistic proportions`;

    const promptDisplay = document.getElementById("promptDisplay");
    promptDisplay.textContent = currentPrompt;
    promptDisplay.style.display = "block";
}

function copyPrompt() {
    if (!currentPrompt) return;

    navigator.clipboard
        .writeText(currentPrompt)
        .then(() => {
            const btn = document.getElementById("copyPromptBtn");
            const originalText = btn.textContent;
            btn.textContent = "Copied!";
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        })
        .catch((err) => {
            console.error("Failed to copy:", err);
            alert("Failed to copy prompt");
        });
}

async function generateMugshot() {
    const generateBtn = document.getElementById("generateBtn");
    const resultContainer = document.getElementById("resultContainer");
    const csrftoken = getCookie("csrftoken");

    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";
    resultContainer.innerHTML =
        '<div class="loading">Generating realistic pencil sketch...<br>First generation may take 5-10 minutes to download models (~19GB)<br>Subsequent generations: 15-20 seconds</div>';

    try {
        // Create composition
        const compositionResponse = await fetch(`${API_BASE}/compositions/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                selected_features: Array.from(selectedFeatures),
            }),
        });

        const composition = await compositionResponse.json();
        currentCompositionId = composition.id;

        // Generate sketch
        const sketchResponse = await fetch(
            `${API_BASE}/compositions/${composition.id}/generate_sketch/`,
            {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
            },
        );

        const result = await sketchResponse.json();

        if (result.image_url) {
            resultContainer.innerHTML = `
                <img src="${result.image_url}" alt="Generated Sketch" class="result-image" id="sketchImage">
                <div class="action-buttons" style="margin-top: 15px;">
                    <button class="btn btn-secondary" onclick="downloadImage('${result.image_url}')">
                        Download Sketch
                    </button>
                    <button class="btn btn-secondary" onclick="showReviseDialog()">
                        Revise Sketch
                    </button>
                    <button class="btn btn-primary" onclick="colorizeSketch()">
                        Colorize
                    </button>
                </div>
            `;
        } else {
            resultContainer.innerHTML =
                '<div class="loading" style="color: #dc3545;">Generation failed. Please try again.</div>';
        }
    } catch (error) {
        console.error("Error generating mugshot:", error);
        resultContainer.innerHTML =
            '<div class="loading" style="color: #dc3545;">Error: ' +
            error.message +
            "</div>";
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "Generate Mugshot";
    }
}

function showReviseDialog() {
    if (!currentCompositionId) {
        alert("No sketch to revise");
        return;
    }

    const revisionPrompt = prompt(
        "Describe changes to make (e.g., 'make nose wider', 'add scar on left cheek'):",
        ""
    );

    if (revisionPrompt !== null) {
        reviseSketch(revisionPrompt);
    }
}

async function reviseSketch(revisionPrompt) {
    const resultContainer = document.getElementById("resultContainer");
    const csrftoken = getCookie("csrftoken");

    resultContainer.innerHTML = '<div class="loading">Revising sketch...</div>';

    try {
        const response = await fetch(
            `${API_BASE}/compositions/${currentCompositionId}/revise_sketch/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    prompt: revisionPrompt,
                    strength: 0.6,
                    quality: "balanced",
                }),
            }
        );

        const result = await response.json();

        if (result.image_url) {
            resultContainer.innerHTML = `
                <img src="${result.image_url}" alt="Revised Sketch" class="result-image" id="sketchImage">
                <div class="action-buttons" style="margin-top: 15px;">
                    <button class="btn btn-secondary" onclick="downloadImage('${result.image_url}')">
                        Download Sketch
                    </button>
                    <button class="btn btn-secondary" onclick="showReviseDialog()">
                        Revise Again
                    </button>
                    <button class="btn btn-primary" onclick="colorizeSketch()">
                        Colorize
                    </button>
                </div>
            `;
        } else {
            resultContainer.innerHTML =
                '<div class="loading" style="color: #dc3545;">Revision failed: ' +
                (result.error || "Unknown error") +
                "</div>";
        }
    } catch (error) {
        console.error("Error revising sketch:", error);
        resultContainer.innerHTML =
            '<div class="loading" style="color: #dc3545;">Error: ' +
            error.message +
            "</div>";
    }
}

async function colorizeSketch() {
    if (!currentCompositionId) {
        alert("No sketch to colorize");
        return;
    }

    const resultContainer = document.getElementById("resultContainer");
    const csrftoken = getCookie("csrftoken");

    resultContainer.innerHTML =
        '<div class="loading">Colorizing sketch...<br>This preserves the sketch structure while adding realistic colors.</div>';

    try {
        const response = await fetch(
            `${API_BASE}/compositions/${currentCompositionId}/colorize/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify({
                    prompt: "",
                    quality: "balanced",
                }),
            }
        );

        const result = await response.json();

        if (result.image_url) {
            resultContainer.innerHTML = `
                <img src="${result.image_url}" alt="Colorized Mugshot" class="result-image">
                <div class="action-buttons" style="margin-top: 15px;">
                    <button class="btn btn-primary" onclick="downloadImage('${result.image_url}')">
                        Download Final Image
                    </button>
                    <button class="btn btn-secondary" onclick="generateMugshot()">
                        Generate New Sketch
                    </button>
                </div>
            `;
        } else {
            resultContainer.innerHTML =
                '<div class="loading" style="color: #dc3545;">Colorization failed: ' +
                (result.error || "Unknown error") +
                "</div>";
        }
    } catch (error) {
        console.error("Error colorizing sketch:", error);
        resultContainer.innerHTML =
            '<div class="loading" style="color: #dc3545;">Error: ' +
            error.message +
            "</div>";
    }
}

function downloadImage(url) {
    const a = document.createElement("a");
    a.href = url;
    a.download = `criminal_face_${Date.now()}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function clearSelection() {
    selectedFeatures.clear();
    currentCompositionId = null;
    document.querySelectorAll(".feature-card").forEach((card) => {
        card.classList.remove("selected");
    });

    document.getElementById("resultContainer").innerHTML = "";
    updateCanvas();
    updateSelectedCount();
}

