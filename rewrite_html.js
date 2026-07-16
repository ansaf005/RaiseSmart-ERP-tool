const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

if (!html.includes('@supabase/supabase-js')) {
    html = html.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>');
}

const init_script = `
const SUPABASE_URL = 'https://ylosjvorcypzomsaxyzz.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlsb3Nqdm9yY3lwem9tc2F4eXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM3NTI3NTYsImV4cCI6MjA5OTMyODc1Nn0.EgC4Z4jn98J01DtUn2Xn5lFut6MBGWjlhYQTcIbkbyE';
const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

window.syncState = async function() {
    if(!S) return;
    const stateToSave = {
        students: S.students, problems: S.problems, mentors: S.mentors, mentorBookings: S.mentorBookings,
        experts: S.experts, expertBookings: S.expertBookings, marks: S.marks, teamChanges: S.teamChanges,
        critical: S.critical, questions: S.questions
    };
    await supabase.from('app_state').upsert({ id: 1, state: stateToSave });
};

async function loadSupabaseState() {
    const { data, error } = await supabase.from('app_state').select('state').eq('id', 1).single();
    if (data && data.state && Object.keys(data.state).length > 0) {
        Object.assign(S, data.state);
    } else {
        await window.syncState(); // first time, save the dummy state
    }
    
    if(!bootEval()) renderLogin();
}
`;

if (!html.includes('SUPABASE_URL')) {
    html = html.replace('var SPECS=', init_script + '\nvar SPECS=');
    html = html.replace('if(!bootEval())renderLogin();', 'loadSupabaseState();');
}

// Global replacement of go(S.tab); inside functions to sync state.
// We will replace `go(S.tab)` with `if(window.syncState) window.syncState(); go(S.tab)` everywhere.
// That is much safer! Wait, `go()` is also used just for navigation, which would trigger unneeded syncs.
// But unneeded syncs are totally fine for a prototype! It's better than missing a sync.
html = html.replace(/go\(S\.tab\)/g, 'if(window.syncState) window.syncState(); go(S.tab)');
html = html.replace(/go\('dpublish'\)/g, 'if(window.syncState) window.syncState(); go(\'dpublish\')');

fs.writeFileSync('index.html', html, 'utf8');
