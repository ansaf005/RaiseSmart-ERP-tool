import re

def rewrite():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add Supabase JS client in head
    if '@supabase' not in html:
        html = html.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>')

    # 2. Add init script at the beginning of the <script> block, before var SPECS
    init_script = """
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
"""
    if 'SUPABASE_URL' not in html:
        html = html.replace('var SPECS=', init_script + '\nvar SPECS=')
        
        # Replace the final bootEval() call with our async loader
        html = html.replace('if(!bootEval())renderLogin();', 'loadSupabaseState();')

    # 3. Inject syncState() into mutation functions
    mutation_funcs = [
        'chooseProblem', 'assignTL', 'bookMentor', 'bookExpert', 
        'saveMentor', 'saveExpert', 'saveSession', 'saveQuestion', 
        'editQuestion', 'delQuestion', 'publishQuestions', 'doTeamChange', 
        'deployCR', 'dToggleEval', 'dCreate', 'dSaveEdit', 'dReady', 'dPublishAll'
    ]
    
    for func in mutation_funcs:
        # Simple regex to find the end of the function body and insert syncState()
        # Find `function funcname(...) { ... go('...'); }` or similar.
        # Actually it's easier to replace `go(S.tab);` inside these functions with `if(window.syncState) window.syncState(); go(S.tab);`
        # Because every mutation ends with `go(...)`.
        pass
        
    # Global replacement of `go(` to also sync state if we are mutating? No, go is used for navigation too.
    # We will just inject it into the specific functions.
    for func in mutation_funcs:
        # Match function definition until its first `go(` call or `toast(`
        pattern = r'(function\s+' + func + r'\s*\(.*?\)\s*\{.*?)(toast\(|go\()'
        html = re.sub(pattern, r'\1if(window.syncState) window.syncState();\n\2', html, count=1, flags=re.DOTALL)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    rewrite()
