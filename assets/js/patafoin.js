document.addEventListener('DOMContentLoaded', async () => {
    console.log("🚀 [Patafoin] v2.1 - Unified Architecture");

    try {
        // --- 1. INITIALISATION ---
        let sb;
        if (typeof supabase === 'undefined') {
            console.warn("⚠️ [Patafoin] Supabase not ready yet, waiting 100ms...");
            await new Promise(r => setTimeout(r, 100));
            if (typeof supabase === 'undefined') {
                const errMsg = '<div class="text-ctp-red p-4 border border-ctp-red rounded">Erreur critique: Impossible de charger le moteur de base de données. Vérifiez votre connexion ou bloqueur de publicité.</div>';
                const container = document.getElementById('topics-container');
                if(container) container.innerHTML = errMsg;
                console.error("❌ [Patafoin] Supabase failed to load from CDN.");
                return;
            }
        }

        const { createClient } = supabase;
        const config = window.SUPABASE_CONFIG;

        if (!config || !config.url || !config.key) {
            console.error("❌ [Patafoin] Config missing.");
            return;
        }

        sb = createClient(config.url, config.key);
        console.log("✅ [Patafoin] Supabase Connected");

        // --- 2. DOM ELEMENTS ---
        const els = {
            btnNewTopic: document.getElementById('btn-new-topic'),
            panelCreate: document.getElementById('create-topic-panel'),
            topicsContainer: document.getElementById('topics-container'),
            detailView: document.getElementById('topic-detail-view'),
            detailHeader: document.getElementById('detail-header'),
            postsContainer: document.getElementById('posts-container')
        };

        // VISUAL FEEDBACK: Enable button
        if (els.btnNewTopic) {
            els.btnNewTopic.classList.remove('opacity-50', 'cursor-not-allowed');
            console.log("✅ [Patafoin] Button activated");
        }

        let currentTopicId = null;

        // --- 3. UTILS ---
        function escapeHTML(str) {
            if (!str) return '';
            return str.replace(/[&<>'"]/g, tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag]));
        }

        function formatDate(dateStr) {
            return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
        }

        // --- 4. LOGIC ---
        async function fetchAndRenderTopics() {
            if(!els.topicsContainer) return;
            
            els.topicsContainer.innerHTML = '<div class="text-center py-12 text-ctp-overlay1 animate-pulse lowercase">chargement...</div>';
            const { data: topics, error } = await sb.from('topics').select('*').order('created_at', { ascending: false });

            if (error) {
                els.topicsContainer.innerHTML = `<div class="text-ctp-red">Erreur: ${error.message}</div>`;
                return;
            }

            if (!topics || topics.length === 0) {
                els.topicsContainer.innerHTML = '<div class="text-center text-ctp-subtext0 italic lowercase">le néant.</div>';
                return;
            }

            els.topicsContainer.innerHTML = '';
            topics.forEach(topic => {
                const div = document.createElement('div');
                div.className = `group cursor-pointer bg-ctp-mantle border border-ctp-surface1 rounded-xl p-6 hover:border-ctp-mauve hover:shadow-[4px_4px_0px_0px_var(--color-ctp-surface1)] transition-all duration-300`;
                div.dataset.topicId = topic.id;
                div.dataset.action = 'open-topic';

                div.innerHTML = `
                    <h3 class="text-xl font-bold text-ctp-text group-hover:text-ctp-mauve transition-colors mb-2 lowercase pointer-events-none">
                        ${escapeHTML(topic.title)}
                    </h3>
                    <div class="flex justify-between text-sm text-ctp-overlay1 lowercase pointer-events-none">
                        <span>par ${escapeHTML(topic.author_name || 'inconnu')}</span>
                        <span>${formatDate(topic.created_at)}</span>
                    </div>
                `;
                els.topicsContainer.appendChild(div);
            });
        }

        async function openTopic(topicId) {
            currentTopicId = topicId;
            const { data: topic } = await sb.from('topics').select('*').eq('id', topicId).single();

            if (!topic) return;

            if(els.topicsContainer) els.topicsContainer.classList.add('hidden');
            if(els.btnNewTopic) els.btnNewTopic.classList.add('hidden');
            if(els.panelCreate) els.panelCreate.classList.add('hidden');
            if(els.detailView) els.detailView.classList.remove('hidden');

            if(els.detailHeader) {
                els.detailHeader.innerHTML = `
                    <h2 class="text-3xl font-bold text-ctp-mauve mb-2 lowercase">${escapeHTML(topic.title)}</h2>
                    <div class="text-ctp-subtext0 lowercase">
                        lancé par <span class="text-ctp-teal">${escapeHTML(topic.author_name)}</span> 
                        le ${formatDate(topic.created_at)}
                    </div>
                `;
            }

            if(els.postsContainer) {
                els.postsContainer.innerHTML = '<div class="text-center py-8 text-ctp-overlay1 animate-pulse">récupération...</div>';
                const { data: posts } = await sb.from('posts').select('*').eq('topic_id', currentTopicId).order('created_at', { ascending: true });

                els.postsContainer.innerHTML = '';
                posts.forEach((post, index) => {
                    const div = document.createElement('div');
                    div.className = `flex flex-col gap-2 p-6 rounded-xl ${index === 0 ? 'bg-ctp-surface0 border border-ctp-mauve/20' : 'bg-ctp-mantle border border-ctp-surface1'}`;
                    div.innerHTML = `
                        <div class="flex justify-between items-baseline mb-2 border-b border-ctp-surface1 pb-2">
                            <span class="font-bold text-ctp-peach lowercase">${escapeHTML(post.author_name)}</span>
                            <span class="text-xs text-ctp-overlay0">${formatDate(post.created_at)}</span>
                        </div>
                        <div class="text-ctp-text normal-case leading-relaxed whitespace-pre-wrap">${escapeHTML(post.content)}</div>
                    `;
                    els.postsContainer.appendChild(div);
                });
            }
        }

        // --- 5. EVENT DELEGATION (CLEAN & ROBUST) ---
        document.addEventListener('click', async (e) => {
            const target = e.target;

            // 1. New Topic Button
            if (target.closest('#btn-new-topic')) {
                console.log("🖱️ [Patafoin] Click New Topic");
                if(els.panelCreate) els.panelCreate.classList.toggle('hidden');
                return;
            }

            // 2. Cancel Button
            if (target.closest('#btn-cancel-topic')) {
                if(els.panelCreate) els.panelCreate.classList.add('hidden');
                return;
            }

            // 3. Back Button
            if (target.closest('#btn-back-home')) {
                if(els.detailView) els.detailView.classList.add('hidden');
                if(els.topicsContainer) els.topicsContainer.classList.remove('hidden');
                if(els.btnNewTopic) els.btnNewTopic.classList.remove('hidden');
                currentTopicId = null;
                fetchAndRenderTopics();
                return;
            }

            // 4. Topic Card (Delegation from container)
            const topicCard = target.closest('[data-action="open-topic"]');
            if (topicCard) {
                const id = topicCard.dataset.topicId;
                openTopic(id);
                return;
            }
        });

        // --- 6. FORMS ---
        const formNew = document.getElementById('form-new-topic');
        if (formNew) {
            formNew.addEventListener('submit', async (e) => {
                e.preventDefault();
                const title = document.getElementById('topic-title').value;
                const author = document.getElementById('topic-author').value || 'Anonyme';
                const content = document.getElementById('topic-content').value;

                const { data: topic, error } = await sb.from('topics').insert([{ title, author_name: author }]).select().single();
                if (error) { alert(error.message); return; }

                await sb.from('posts').insert([{ topic_id: topic.id, author_name: author, content }]);

                formNew.reset();
                els.panelCreate.classList.add('hidden');
                fetchAndRenderTopics();
            });
        }

        const formReply = document.getElementById('form-reply');
        if (formReply) {
            formReply.addEventListener('submit', async (e) => {
                e.preventDefault();
                if (!currentTopicId) return;
                const author = document.getElementById('reply-author').value || 'Anonyme';
                const content = document.getElementById('reply-content').value;

                await sb.from('posts').insert([{ topic_id: currentTopicId, author_name: author, content }]);

                document.getElementById('reply-content').value = '';
                openTopic(currentTopicId);
            });
        }

        // Initial Load
        fetchAndRenderTopics();

    } catch (err) {
        console.error("🔥 [Patafoin] CRASH:", err);
    }
});