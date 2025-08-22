import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from bot_manager import BotManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize bot manager
bot_manager = BotManager()

@app.route('/')
def index():
    """Main page with token input form"""
    bot_status = bot_manager.get_status()
    return render_template('index.html', bot_status=bot_status)

@app.route('/premium')
def premium():
    """Premium page - Under maintenance"""
    return render_template('maintenance.html', feature="Premium Features")

@app.route('/admin')
def admin():
    """Admin page - Under maintenance"""
    return render_template('maintenance.html', feature="Admin Panel")

@app.route('/start_bot', methods=['POST'])
def start_bot():
    """Start the Discord bot with the provided token"""
    token = request.form.get('token', '').strip()
    
    if not token:
        flash('Por favor ingresa un token de Discord bot', 'error')
        return redirect(url_for('index'))
    
    # Basic token format validation
    if len(token) < 50:
        flash('Formato de token inválido. Los tokens de Discord bots suelen ser más largos.', 'error')
        return redirect(url_for('index'))
    
    # Check if bot is already running
    if bot_manager.is_running():
        flash('El bot ya está ejecutándose. Deténlo primero antes de iniciar con un nuevo token.', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Start the bot (always free version now)
        success, message = bot_manager.start_bot(token)
        if success:
            flash('¡Bot iniciado exitosamente!', 'success')
        else:
            flash(f'Error al iniciar bot: {message}', 'error')
    except Exception as e:
        flash(f'Error iniciando bot: {str(e)}', 'error')
        logging.error(f"Error starting bot: {e}")
    
    return redirect(url_for('index'))

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    """Stop the running Discord bot"""
    try:
        success, message = bot_manager.stop_bot()
        if success:
            flash('¡Bot detenido exitosamente!', 'success')
        else:
            flash(f'Error al detener bot: {message}', 'error')
    except Exception as e:
        flash(f'Error deteniendo bot: {str(e)}', 'error')
        logging.error(f"Error stopping bot: {e}")
    
    return redirect(url_for('index'))

@app.route('/bot_status')
def bot_status():
    """API endpoint to get bot status"""
    return jsonify(bot_manager.get_status())

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', error='Página no encontrada'), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Internal error: {error}")
    return render_template('index.html', error='Error interno del servidor'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)