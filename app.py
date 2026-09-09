from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_premium = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    histories = db.relationship('History', backref='user', lazy=True, cascade='all, delete-orphan')

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    theme = db.Column(db.String(200), nullable=False)
    titles = db.Column(db.Text, nullable=False)  # JSON list
    hooks = db.Column(db.Text, nullable=False)
    ctas = db.Column(db.Text, nullable=False)
    descriptions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def generate_content_ideas(theme):
    """Gera ideias de conteúdo baseadas no tema usando templates inteligentes."""
    theme = theme.strip()
    theme_title = theme.title() if theme.islower() else theme
    
    # Templates de títulos
    title_templates = [
        f"O Segredo de {theme} que Ninguém Te Conta",
        f"5 Erros Fatais em {theme} (e Como Evitar)",
        f"Como Dominar {theme} em 2025: Guia Completo",
        f"{theme_title}: Do Zero ao Resultado em 30 Dias",
        f"Por Que Seu {theme} Não Está Funcionando?",
        f"A Verdade Sobre {theme} Que Muda Tudo",
        f"7 Dicas Infalíveis de {theme} Para Iniciantes",
        f"{theme_title} Explicado de Forma Simples",
        f"O Método Comprovado Para Lucrar com {theme}",
        f"Transforme Seu {theme} Hoje Mesmo"
    ]
    
    # Templates de hooks (primeiros 3 segundos)
    hook_templates = [
        f"Você está perdendo dinheiro com {theme} e nem sabe...",
        f"Pare tudo! Isso sobre {theme} vai mudar sua vida.",
        f"Ninguém fala sobre esse erro em {theme}...",
        f"Em 3 segundos: o truque de {theme} que viralizou.",
        f"Se você faz {theme} assim, está fazendo errado.",
        f"Atenção: o mercado de {theme} nunca mais será o mesmo.",
        f"Eu quase desisti de {theme} até descobrir isso...",
        f"O que os experts de {theme} não querem que você saiba.",
        f"Isso aqui sobre {theme} está bombando agora.",
        f"3 segundos para entender por que seu {theme} falha."
    ]
    
    # Templates de CTAs
    cta_templates = [
        f"Salve este post e comece a aplicar em {theme} hoje!",
        f"Comente 'EU QUERO' se você quer dominar {theme}!",
        f"Siga para mais dicas diárias sobre {theme}!",
        f"Link na bio para o guia completo de {theme}!",
        f"Marque um amigo que precisa ver isso sobre {theme}!",
        f"Qual sua maior dúvida sobre {theme}? Comenta aí!",
        f"Clique no link e transforme seu {theme} agora!",
        f"Compartilhe se você ama conteúdo de {theme}!",
        f"Ative o sininho para não perder nada de {theme}!",
        f"Baixe o checklist gratuito de {theme} na bio!"
    ]
    
    # Templates de descrições
    desc_templates = [
        f"Descubra as estratégias mais poderosas de {theme} que estão gerando resultados reais em 2025. Neste conteúdo você vai aprender o passo a passo para aplicar imediatamente e ver diferença.",
        f"Cansado de ver todo mundo avançando em {theme} enquanto você fica para trás? Este guia prático mostra exatamente o que fazer, sem enrolação e com exemplos reais.",
        f"O universo de {theme} muda rápido. Aqui estão as tendências, ferramentas e mentalidade que separam quem cresce de quem fica estagnado. Conteúdo direto ao ponto.",
        f"Se você está começando em {theme} ou quer elevar o nível, este material foi feito para você. Dicas acionáveis, erros comuns e o caminho mais curto para resultados.",
        f"Muita gente complica {theme}. A verdade é que com o método certo qualquer pessoa pode ter sucesso. Veja como simplificar e acelerar seus resultados.",
        f"Análise completa sobre {theme}: o que funciona, o que não funciona e como você pode aplicar tudo isso na prática ainda esta semana.",
        f"De iniciante a avançado: o roadmap definitivo de {theme} que eu gostaria de ter tido quando comecei. Salve e volte sempre que precisar.",
        f"Conteúdo valioso sobre {theme} baseado em experiência real e dados atuais. Sem teoria vazia, só o que realmente gera impacto.",
        f"Quer resultados consistentes com {theme}? Este conteúdo reúne as melhores práticas do mercado de forma clara e aplicável.",
        f"Tudo o que você precisa saber sobre {theme} em um só lugar. Ideal para quem quer economizar tempo e ir direto ao que importa."
    ]
    
    # Selecionar 5-7 de cada aleatoriamente
    titles = random.sample(title_templates, min(6, len(title_templates)))
    hooks = random.sample(hook_templates, min(6, len(hook_templates)))
    ctas = random.sample(cta_templates, min(6, len(cta_templates)))
    descriptions = random.sample(desc_templates, min(5, len(desc_templates)))
    
    return {
        'titles': titles,
        'hooks': hooks,
        'ctas': ctas,
        'descriptions': descriptions
    }
@app.route('/')

def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session.get('user_id'))
    if not user:
        return redirect(url_for('login'))

    if user.email == "jademattosmafort3@gmail.com":
        user.is_premium = True
        db.session.commit()

    if not user.is_premium:
        return redirect('https://pay.hotmart.com/P107487785L')

    return render_template('index.html', user_name=session.get('user_name'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        if not name or not email or not password:
            flash('Preencha todos os campos.', 'error')
            return render_template('register.html')
        
        if password != confirm:
            flash('As senhas não coincidem.', 'error')
            return render_template('register.html')
        

        if len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'error')
            return render_template('register.html')
        
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        
        flash('E-mail ou senha incorretos.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da conta.', 'success')
    return redirect(url_for('login'))

@app.route('/generate', methods=['POST'])
def generate():
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    data = request.get_json()
    theme = data.get('theme', '').strip()
    
    if not theme:
        return jsonify({'error': 'Informe um tema'}), 400
    
    if len(theme) > 150:
        return jsonify({'error': 'Tema muito longo'}), 400
    
    ideas = generate_content_ideas(theme)
    
    # Salvar no histórico
    history = History(
        user_id=session['user_id'],
        theme=theme,
        titles=json.dumps(ideas['titles'], ensure_ascii=False),
        hooks=json.dumps(ideas['hooks'], ensure_ascii=False),
        ctas=json.dumps(ideas['ctas'], ensure_ascii=False),
        descriptions=json.dumps(ideas['descriptions'], ensure_ascii=False)
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'theme': theme,
        'ideas': ideas,
        'history_id': history.id
    })

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    histories = History.query.filter_by(user_id=session['user_id']).order_by(History.created_at.desc()).all()
    
    history_list = []
    for h in histories:
        history_list.append({
            'id': h.id,
            'theme': h.theme,
            'titles': json.loads(h.titles),
            'hooks': json.loads(h.hooks),
            'ctas': json.loads(h.ctas),
            'descriptions': json.loads(h.descriptions),
            'created_at': h.created_at.strftime('%d/%m/%Y %H:%M')
        })
    
    return render_template('history.html', histories=history_list, user_name=session.get('user_name'))

@app.route('/history/<int:history_id>')
def history_detail(history_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    h = History.query.filter_by(id=history_id, user_id=session['user_id']).first_or_404()
    
    return jsonify({
        'id': h.id,
        'theme': h.theme,
        'titles': json.loads(h.titles),
        'hooks': json.loads(h.hooks),
        'ctas': json.loads(h.ctas),
        'descriptions': json.loads(h.descriptions),
      'created_at': h.created_at.strftime('%d/%m/%Y %H:%M')
    })

@app.route('/history/<int:history_id>/delete', methods=['POST'])
def delete_history(history_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    h = History.query.filter_by(id=history_id, user_id=session['user_id']).first()
    if h:
        db.session.delete(h)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Não encontrado'}), 404
@app.route('/webhook/kiwify', methods=['POST'])
def webhook_kiwify():
    payload = request.json
    order_status = payload.get("order_status")
    if order_status == "paid":
        customer_email = payload.get("Customer", {}).get("email")
        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_premium = True
            db.session.commit()
    return jsonify({"status": "received"}), 200

with app.app_context():
    db.create_all()
    try:
        db.session.execute(db.text('ALTER TABLE user ADD COLUMN is_premium BOOLEAN DEFAULT 0'))
        db.session.commit()
    except Exception:
        db.session.rollback()

with app.app_context():
    db.create_all()
    try:
        db.session.execute(db.text('ALTER TABLE user ADD COLUMN is_premium BOOLEAN DEFAULT 0'))
        db.session.commit()
    except Exception:
        db.session.rollback()


@app.route('/webhook/kiwify', methods=['POST'])
def kiwify_webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    event_type = data.get('event')
    customer = data.get('Customer', {})
    email = customer.get('email')
    
    print(f"Webhook recebido da Kiwify: {event_type} para o e-mail {email}")

    if event_type in ['subscription_canceled', 'subscription_expired', 'charge_back']:
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_premium = False
            db.session.commit()
            print(f"Usuário {email} desativado.")
@app.route('/webhook/hotmart', methods=['POST'])
def hotmart_webhook():
    dados = request.get_json()
    if not dados:
        return jsonify({'status': 'no data'}), 400

    evento = dados.get('event')
    if evento == 'PURCHASE_APPROVED':
        email_comprador = dados.get('data', {}).get('buyer', {}).get('email')
        if email_comprador:
            user = User.query.filter_by(email=email_comprador).first()
            if user:
                user.is_premium = True
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Access granted'}), 200

    return jsonify({'status': 'ignored'}), 200
 