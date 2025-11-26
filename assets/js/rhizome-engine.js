/**
 * RHIZOME ENGINE v6.0 - "Orbital Physics Edition"
 * Architecture: Nucleus (Roots) + Cytoplasm Orbit (Spores)
 * Physics: d3.forceRadial with split radii
 */

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("rhizome-viz");
    const tooltip = document.getElementById("rhizome-tooltip");
    
    if (!container || !tooltip) return;

    // --- CONFIGURATION ---
    const CONFIG = {
        zoomMin: 0.1,
        zoomMax: 3,
        // Physique Orbitale
        orbitRadius: 400,    // Rayon de l'orbite des Spores
        nucleusRadius: 0,    // Rayon du noyau (Centre)
        radialStrength: 0.8, // Force d'attraction vers le rayon défini
        
        // Forces répulsives
        chargeStrength: -200, // Répulsion plus forte pour bien séparer l'anneau
        collidePadding: 15,   // Padding confortable
        
        // Liens (Uniquement Internes)
        linkDistance: 100,
        
        // Rendu
        velocityDecay: 0.6,   // Friction élevée pour stabiliser l'orbite
        initialAlpha: 1,
        charWidth: 9,
        basePadding: 24,
        nodeHeight: 32
    };

    let state = {
        width: container.clientWidth,
        height: container.clientHeight,
        nodes: [],
        links: [],
        filters: { internal: true, external: true },
        colors: { surface2: '#5b6078', text: '#cad3f5' }
    };

    // --- D3 SETUP ---
    const svg = d3.select("#rhizome-viz")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", [0, 0, state.width, state.height])
        .style("cursor", "grab")
        .on("click", (e) => {
            if(e.target.tagName === 'svg') hideTooltip();
        });

    const world = svg.append("g").attr("class", "world-layer");
    const linkLayer = world.append("g").attr("class", "links");
    const nodeLayer = world.append("g").attr("class", "nodes");

    // Zoom Centré
    const zoom = d3.zoom()
        .scaleExtent([CONFIG.zoomMin, CONFIG.zoomMax])
        .on("zoom", (e) => {
            world.attr("transform", e.transform);
            hideTooltip();
        });

    svg.call(zoom)
       .call(zoom.transform, d3.zoomIdentity.translate(state.width/2, state.height/2).scale(0.55));

    // Simulation Physique Orbitale
    let simulation = d3.forceSimulation()
        .force("charge", d3.forceManyBody().strength(CONFIG.chargeStrength))
        // La magie opère ici : Deux zones d'attraction distinctes selon le type
        .force("r", d3.forceRadial(
            d => d.type === 'internal' ? CONFIG.nucleusRadius : CONFIG.orbitRadius, 
            0, // x center
            0  // y center
        ).strength(CONFIG.radialStrength))
        .velocityDecay(CONFIG.velocityDecay);

    // --- DATA LOADING ---
    d3.json("index.json").then(raw => {
        const sourceNodes = raw.nodes || raw;
        
        const processedNodes = sourceNodes.map(d => {
            // Calcul Géométrie Capsule
            const label = d.title || d.id || "???";
            const displayLabel = label.length > 25 ? label.substring(0, 24) + "…" : label;
            const w = (displayLabel.length * CONFIG.charWidth) + CONFIG.basePadding;
            const collisionRadius = Math.sqrt(Math.pow(w/2, 2) + Math.pow(CONFIG.nodeHeight/2, 2));

            return {
                ...d,
                label: displayLabel,
                fullTitle: d.title,
                width: w,
                height: CONFIG.nodeHeight,
                collisionR: collisionRadius,
                // Dispersion initiale aléatoire pour éviter le "Big Bang" visuel
                x: (Math.random() - 0.5) * 1000,
                y: (Math.random() - 0.5) * 1000
            };
        });

        // Génération stricte : Uniquement les liens Internes -> Internes
        const processedLinks = generateNucleusMesh(processedNodes, raw.links);

        state.nodes = processedNodes;
        state.links = processedLinks;

        // Mise à jour forces dépendantes des données
        simulation.force("collide", d3.forceCollide()
            .radius(d => d.collisionR + CONFIG.collidePadding)
            .iterations(3)
        );

        simulation.force("link", d3.forceLink(state.links)
            .id(d => d.id)
            .distance(CONFIG.linkDistance)
            .strength(0.5)
        );

        updateStats();
        setupControls();
        render();

    }).catch(console.error);

    // --- TOPOLOGY UTILS ---
    function generateNucleusMesh(nodes, explicitLinks = []) {
        // Stratégie : On ignore totalement les connexions vers les "external" (Spores).
        // Les Spores doivent flotter librement.
        
        let links = [];
        const internals = nodes.filter(n => n.type === 'internal');
        
        // 1. Connexions explicites (si les deux bouts sont internes)
        if(explicitLinks) {
            explicitLinks.forEach(l => {
                const sourceNode = nodes.find(n => n.id === (l.source.id || l.source));
                const targetNode = nodes.find(n => n.id === (l.target.id || l.target));
                if(sourceNode?.type === 'internal' && targetNode?.type === 'internal') {
                    links.push({ source: l.source, target: l.target });
                }
            });
        }

        // 2. Mesh Séquentiel (Spine) pour garantir que le noyau se tient
        // Relie chaque interne au suivant pour former une chaîne/boucle
        for (let i = 0; i < internals.length - 1; i++) {
            links.push({ source: internals[i].id, target: internals[i+1].id });
        }
        
        // Fermer la boucle pour solidifier le noyau
        if(internals.length > 2) {
             links.push({ source: internals[internals.length-1].id, target: internals[0].id });
        }

        return links;
    }

    // --- RENDER ---
    function render() {
        const activeNodes = state.nodes.filter(d => state.filters[d.type]);
        const activeIds = new Set(activeNodes.map(d => d.id));
        
        // Filtrage des liens : double sécurité
        const activeLinks = state.links.filter(l => 
            activeIds.has(l.source.id || l.source) && activeIds.has(l.target.id || l.target)
        );

        // LINKS (Uniquement Mesh du Noyau)
        const links = linkLayer.selectAll(".link").data(activeLinks, d => `${d.source.id}-${d.target.id}`);
        links.exit().remove();
        const linkEnter = links.enter().append("line")
            .attr("class", "link")
            .attr("stroke", state.colors.surface2)
            .attr("stroke-width", 2)
            .attr("opacity", 0.3); // Très subtil pour laisser respirer le noyau
        const linksMerged = linkEnter.merge(links);

        // NODES
        const nodes = nodeLayer.selectAll(".node-group").data(activeNodes, d => d.id);
        nodes.exit().remove();

        const nodeEnter = nodes.enter().append("g")
            .attr("class", "node-group")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        // 1. CAPSULE
        nodeEnter.append("rect")
            .attr("class", d => `node-body ${d.type === 'internal' ? 'node-root' : 'node-spore'}`)
            .attr("width", d => d.width)
            .attr("height", d => d.height)
            .attr("x", d => -d.width / 2)
            .attr("y", d => -d.height / 2)
            .attr("rx", d => d.height / 2)
            .attr("ry", d => d.height / 2);

        // 2. TEXTE
        nodeEnter.append("text")
            .text(d => d.label)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .attr("font-family", "'JetBrains Mono', monospace")
            .attr("font-weight", "bold")
            .attr("font-size", "11px")
            .style("pointer-events", "none") 
            .style("fill", state.colors.text)
            .style("opacity", 0.95);

        // Events
        nodeEnter
            .on("mouseenter", (e, d) => showTooltip(e, d))
            .on("mouseleave", hideTooltip)
            .on("click", (e, d) => {
                if(d.url) window.open(d.url, d.type === 'external' ? '_blank' : '_self');
            });

        const nodesMerged = nodeEnter.merge(nodes);

        // Tick loop
        simulation.nodes(activeNodes).on("tick", () => {
            linksMerged
                .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);

            nodesMerged.attr("transform", d => `translate(${d.x},${d.y})`);
        });
        
        simulation.force("link").links(activeLinks);
        simulation.alpha(CONFIG.initialAlpha).restart();
    }

    // --- TOOLTIP ---
    function showTooltip(event, d) {
        const labelText = tooltip.querySelector('.label-text');
        if(labelText) labelText.textContent = d.fullTitle || d.label;

        const transform = d3.zoomTransform(svg.node());
        // Pas besoin de complexité ici car le SVG est centré via viewBox/Zoom
        // Mais on utilise applyX/Y pour être précis par rapport au DOM HTML du tooltip
        const screenX = transform.applyX(d.x);
        const screenY = transform.applyY(d.y);

        tooltip.style.left = `${screenX}px`;
        tooltip.style.top = `${screenY + (d.height/2 * transform.k) + 12}px`; 
        
        tooltip.classList.remove('opacity-0', 'pointer-events-none');
        d3.select(event.currentTarget).select("rect").classed("is-hovered", true);
    }

    function hideTooltip() {
        tooltip.classList.add('opacity-0', 'pointer-events-none');
        d3.selectAll(".node-body").classed("is-hovered", false);
    }

    // --- CONTROLS ---
    function setupControls() {
        document.getElementById("filter-internal")?.addEventListener("click", () => {
            state.filters.internal = !state.filters.internal; render();
        });
        document.getElementById("filter-external")?.addEventListener("click", () => {
            state.filters.external = !state.filters.external; render();
        });
    }

    function updateStats() {
        const el = document.getElementById("stat-nodes");
        if(el) el.textContent = state.nodes.length;
    }
    
    // --- DRAG ---
    // Note: Le drag doit "réchauffer" la simulation pour que la physique orbitale reprenne le dessus
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
        d3.select(this).style("cursor", "grabbing").raise(); 
        hideTooltip(); 
    }
    function dragged(event, d) { d.fx = event.x; d.fy = event.y; }
    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
        d3.select(this).style("cursor", "grab");
    }
});