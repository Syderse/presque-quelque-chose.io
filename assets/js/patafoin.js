document.addEventListener('DOMContentLoaded', async () => {
    console.log("🟢 Patafoin ronronne...");

    // --- 1. CONFIGURATION & INIT ---
    let sb;
    const dom = {
        tree: document.getElementById('system-tree'),
        btnRoot: document.getElementById('btn-create-root'),
        panelRoot: document.getElementById('root-form-panel'),
        formRoot: document.getElementById('form-new-topic'),
        btnCancelRoot: document.getElementById('btn-cancel-root'),
        // Templates
        tmplTopic: document.getElementById('tmpl-topic'),
        tmplPost: document.getElementById('tmpl-post'),
        tmplReplyForm: document.getElementById('tmpl-reply-form')
    };

    // Initialisation Supabase
    try {
        if (typeof supabase === 'undefined') throw new Error("Supabase Library Missing");
        sb = supabase.createClient(window.SUPABASE_CONFIG.url, window.SUPABASE_CONFIG.key);
    } catch (e) {
        dom.tree.innerHTML = `<div class="text-ctp-red font-mono p-4 border border-ctp-red bg-ctp-mantle">Oups, impossible de se connecter : ${e.message}</div>`;
        return;
    }

    // --- 2. FONCTIONS UTILITAIRES ---
    const utils = {
        hex: (str) => str ? str.split('-')[0] : '????',
        date: (str) => new Date(str).toISOString().replace('T', ' ').substring(0, 16),
        escape: (str) => (str || '').replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]))
    };

    // --- 3. MOTEUR DE RENDU RÉCURSIF (CORRIGÉ) ---

    /**
     * Construit l'arbre hiérarchique.
     * @param {Array} flatPosts - La liste des posts
     * @param {String|null} relativeRootId - Si un post a ce parent_id, il devient une racine locale.
     */
    function buildHierarchy(flatPosts, relativeRootId = null) {
        const map = {};
        const roots = [];

        // 1. Indexation
        flatPosts.forEach(post => {
            post.children = [];
            map[post.id] = post;
        });

        // 2. Assemblage
        flatPosts.forEach(post => {
            // Cas A : C'est une réponse directe au sujet (Racine relative)
            // On vérifie cela AVANT de chercher le parent dans la map, car le parent (RootPost) n'est PAS dans flatPosts
            if (post.parent_id === relativeRootId && relativeRootId !== null) {
                roots.push(post);
            }
            // Cas B : C'est une réponse à une réponse (Enfant standard)
            // Le parent doit exister dans la map (donc être une réponse aussi)
            else if (post.parent_id && map[post.parent_id]) {
                map[post.parent_id].children.push(post);
            }
            // Cas C : C'est une racine absolue (Topic legacy ou erreur de données)
            else if (!post.parent_id) {
                roots.push(post);
            }
            // Cas D : Orphelin réel (Parent supprimé ou introuvable)
            else {
                console.warn(`message orphelin détecté : ${post.id}`);
            }
        });

        return roots;
    }

    // Rendu d'un Post (Noeud de l'arbre)
    function renderNode(post, depth = 0) {
        const clone = dom.tmplPost.content.cloneNode(true);

        // Injection Données
        clone.querySelector('.slot-author').textContent = post.author_name || 'anonyme';
        clone.querySelector('.slot-date').textContent = utils.date(post.created_at);
        clone.querySelector('.slot-id').textContent = `0x${utils.hex(post.id)}`;
        clone.querySelector('.slot-content').innerHTML = utils.escape(post.content);

        // Styling Dynamique
        const connector = clone.querySelector('.line-connector');
        connector.classList.add(`depth-${depth % 6}`);

        // Bouton Répondre
        const btnReply = clone.querySelector('.btn-reply-trigger');
        btnReply.dataset.id = post.id;
        btnReply.dataset.topicId = post.topic_id;

        // Récursion
        const subContainer = clone.querySelector('.sub-replies');
        if (post.children && post.children.length > 0) {
            post.children.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
                .forEach(child => {
                    subContainer.appendChild(renderNode(child, depth + 1));
                });
        }

        return clone;
    }

    // Rendu d'un Topic (Dossier Racine)
    function renderTopic(topic) {
        const clone = dom.tmplTopic.content.cloneNode(true);

        clone.querySelector('.slot-title').textContent = topic.title;
        clone.querySelector('.slot-meta').textContent = `par ${topic.root_author || 'anonyme'}`;
        clone.querySelector('.slot-content').innerHTML = utils.escape(topic.content);

        // Bouton répondre au topic (cible le Root Post ID)
        const btnReply = clone.querySelector('.btn-reply-trigger');
        btnReply.dataset.id = topic.root_post_id;
        btnReply.dataset.topicId = topic.id;

        const treeContainer = clone.querySelector('.replies-tree');

        if (topic.children && topic.children.length > 0) {
            topic.children.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
                .forEach(child => {
                    treeContainer.appendChild(renderNode(child, 0));
                });
        } else {
            treeContainer.innerHTML = '<div class="text-ctp-surface2 text-xs italic pl-4 border-l border-dashed border-ctp-surface1 opacity-50">aucune réponse pour le moment...</div>';
        }

        return clone;
    }

    // Fonction Principale de Chargement
    async function loadSystem() {
        dom.tree.innerHTML = '<div class="text-ctp-blue font-mono pl-2">chargement...</div>';

        // 1. Fetch Topics
        const { data: topics, error: errT } = await sb.from('topics').select('*').order('created_at', { ascending: false });
        if (errT) return console.error(errT);

        // 2. Fetch Posts
        const { data: posts, error: errP } = await sb.from('posts').select('*');
        if (errP) return console.error(errP);

        const fullTree = [];

        // 3. Assemblage
        topics.forEach(t => {
            const allTopicPosts = posts.filter(p => p.topic_id === t.id);

            // Le Root Post est celui sans parent
            const rootPost = allTopicPosts.find(p => p.parent_id === null);

            // Les réponses sont tout sauf le Root Post
            const replies = allTopicPosts.filter(p => p.id !== rootPost?.id);

            // Objet Topic enrichi
            const topicObj = {
                ...t,
                content: rootPost ? rootPost.content : '[contenu introuvable]',
                root_author: rootPost ? rootPost.author_name : 'unknown',
                root_post_id: rootPost ? rootPost.id : null,
                children: [],
                type: 'topic'
            };

            // CORRECTION CRITIQUE : On passe l'ID du RootPost comme "Racine Relative"
            // Ainsi, buildHierarchy sait que les posts ayant parent_id === rootPost.id sont les premiers enfants
            if (rootPost) {
                topicObj.children = buildHierarchy(replies, rootPost.id);
            }

            fullTree.push(topicObj);
        });

        // Rendu DOM
        dom.tree.innerHTML = '';
        if (fullTree.length === 0) {
            dom.tree.innerHTML = '<div class="text-ctp-overlay0 pl-2">aucun sujet pour le moment. patafoin chafouine </div>';
            return;
        }

        fullTree.forEach(topic => {
            dom.tree.appendChild(renderTopic(topic));
        });
    }

    // --- 4. GESTION DES INTERACTIONS ---

    dom.btnRoot?.addEventListener('click', () => {
        dom.panelRoot.classList.toggle('hidden');
        if (!dom.panelRoot.classList.contains('hidden')) {
            document.getElementById('topic-title').focus();
        }
    });

    // --- AUTO-OUVERTURE DEPUIS ARTICLE ---
    // Si on arrive avec ?sujet=... on pré-remplit et ouvre le formulaire
    const urlParams = new URLSearchParams(window.location.search);
    const sujetFromUrl = urlParams.get('sujet');
    if (sujetFromUrl && dom.panelRoot && dom.formRoot) {
        const titleInput = document.getElementById('topic-title');
        const contentTextarea = document.getElementById('topic-content');

        // Pré-remplir le titre avec mention de l'article source
        titleInput.value = `À propos de « ${sujetFromUrl} »`;

        // Ouvrir le panneau
        dom.panelRoot.classList.remove('hidden');

        // Focus sur le contenu (le titre est déjà rempli)
        contentTextarea?.focus();

        // Nettoyer l'URL pour éviter les re-soumissions accidentelles
        window.history.replaceState({}, '', window.location.pathname);
    }

    dom.btnCancelRoot?.addEventListener('click', () => {
        dom.panelRoot.classList.add('hidden');
    });

    // Soumission Nouveau Topic
    dom.formRoot?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btnSubmit = dom.formRoot.querySelector('button[type="submit"]');
        const originalText = btnSubmit.textContent;
        btnSubmit.textContent = "[en cours...]";
        btnSubmit.disabled = true;

        const title = document.getElementById('topic-title').value;
        const author = document.getElementById('topic-author').value || 'anonyme';
        const content = document.getElementById('topic-content').value;

        try {
            // Création Topic
            const { data: topicData, error: topicError } = await sb.from('topics').insert([{ title: title }]).select().single();
            if (topicError) throw new Error(topicError.message);

            // Création Root Post
            const { error: postError } = await sb.from('posts').insert([{
                topic_id: topicData.id,
                parent_id: null,
                author_name: author,
                content: content
            }]);

            if (postError) throw new Error(postError.message);

            dom.formRoot.reset();
            dom.panelRoot.classList.add('hidden');
            loadSystem();
        } catch (err) {
            alert(`patafoin s'emmêle les pattes : ${err.message}`);
        } finally {
            btnSubmit.textContent = originalText;
            btnSubmit.disabled = false;
        }
    });

    // Clics (Répondre / Annuler)
    dom.tree.addEventListener('click', (e) => {
        const target = e.target;

        if (target.classList.contains('btn-reply-trigger')) {
            e.preventDefault();
            document.querySelectorAll('.reply-form').forEach(el => el.remove());

            const parentId = target.dataset.id;
            const topicId = target.dataset.topicId;

            if (!parentId || !topicId) return alert("vous ne souhaitez pas écrire ici.");

            const formClone = dom.tmplReplyForm.content.cloneNode(true);
            const form = formClone.querySelector('form');
            form.dataset.parentId = parentId;
            form.dataset.topicId = topicId;
            formClone.querySelector('.slot-target').textContent = `0x${utils.hex(parentId)}`;

            const details = target.closest('details');
            const wrapper = target.closest('.node-wrapper');

            if (details && !wrapper) {
                // Si on répond au Topic lui-même, on insert en haut de la liste des réponses
                const tree = details.querySelector('.replies-tree');
                tree.insertBefore(formClone, tree.firstChild);
            } else {
                // Si on répond à un Post, on insert juste après lui
                target.parentNode.appendChild(formClone);
            }
            form.querySelector('textarea').focus();
        }

        if (target.classList.contains('btn-cancel')) {
            target.closest('form').remove();
        }
    });

    // Soumission Réponse
    dom.tree.addEventListener('submit', async (e) => {
        if (!e.target.classList.contains('reply-form')) return;
        e.preventDefault();

        const form = e.target;
        const btn = form.querySelector('button[type="submit"]');
        btn.textContent = "...";
        btn.disabled = true;

        const content = form.content.value;
        const author = form.author.value || 'anonyme';
        const parentId = form.dataset.parentId;
        const topicId = form.dataset.topicId;

        const { error } = await sb.from('posts').insert([{
            topic_id: topicId,
            parent_id: parentId,
            author_name: author,
            content: content
        }]);

        if (error) {
            alert(`Impossible d'envoyer : ${error.message}`);
            btn.textContent = "[rentez le coup]";
            btn.disabled = false;
        } else {
            form.remove();
            loadSystem();
        }
    });

    loadSystem();
});
