from flask import Flask, render_template, send_file, url_for, request 
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os # Para manipulação de caminhos
from matplotlib.animation import PillowWriter

app = Flask(__name__, template_folder='pages')

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_gif')
def gerar_gif():
    gif_path = os.path.join(STATIC_FOLDER, "simulacao.gif")

    try:
        carga_val_1_nc = float(request.args.get('valor_carga1', 1.0)) 
        carga_val_2_nc = float(request.args.get('valor_carga2', 1.0))
    except (ValueError, TypeError):
        carga_val_1_nc = 1.0
        carga_val_2_nc = 1.0




    # --- Código da Simulação ---
    x_min, x_max = -5, 5
    y_min, y_max = -5, 5
    grid_points = 50 # Reduzir para testes mais rápidos, se necessário (ex: 50)
    x = np.linspace(x_min, x_max, grid_points)
    y = np.linspace(y_min, y_max, grid_points)
    X, Y = np.meshgrid(x, y)
    k = 8.9875517923e9  # Constante de Coulomb
    epsilon = 1e-9      # Pequena constante para evitar divisão por zero
    num_frames = 20     # Reduzir para testes mais rápidos, se necessário (ex: 10)

    fig, ax = plt.subplots(figsize=(6, 6))

    plt.style.use('seaborn-v0_8-whitegrid')


    def update(i):
        ax.clear()
        ax.set_facecolor('none')  # Faz o fundo do gráfico ficar transparente
        # Animação mais suave e valores de carga mais interessantes
        angle = i * 2 * np.pi / num_frames # Variação angular para movimento
        pos_y1 = 2 * np.sin(angle)
        pos_y2 = 2 * np.cos(angle) # Movimento diferente para a segunda carga

        # Valores de carga que variam com o tempo (exemplo)
        # carga_valor_1 = (1 + 0.5 * np.sin(angle)) * 1e-9  # nC para C
        # carga_valor_2 = (1 + 0.5 * np.cos(angleלילה)) * -1e-9 # nC para C, carga oposta
        
        # Usando valores fixos para simplificar, mas você pegaria do request.args
        carga_valor_1 = carga_val_1_nc * 1e-9
        carga_valor_2 = carga_val_2_nc * 1e-9



        charges = np.array([
            [2, pos_y1, carga_valor_1],  # Carga 1: x=2, y varia, valor varia
            [-2, pos_y2, carga_valor_2] # Carga 2: x=-2, y varia, valor varia (oposto)
        ])
        
        potential = np.zeros_like(X)
        Ex = np.zeros_like(X)
        Ey = np.zeros_like(X)

        for charge_idx, charge_props in enumerate(charges):
            qx, qy, q_value = charge_props
            # Evitar que as cargas fiquem exatamente sobre pontos da grade se qx, qy forem discretos
            r_sq = (X - qx)**2 + (Y - qy)**2 + epsilon**2 
            r = np.sqrt(r_sq)
            
            potential += k * q_value / r
            Ex += k * q_value * (X - qx) / r**3
            Ey += k * q_value * (Y - qy) / r**3
        
        # Normalizar campos para streamplot não ficar muito denso
        magnitude = np.sqrt(Ex**2 + Ey**2)
        # Evitar divisão por zero na normalização
        Ex_norm = np.divide(Ex, magnitude, out=np.zeros_like(Ex), where=magnitude!=0)
        Ey_norm = np.divide(Ey, magnitude, out=np.zeros_like(Ey), where=magnitude!=0)

        # Contourf para potencial
        contour_fill = ax.contourf(X, Y, potential, levels=50, cmap='viridis')
        # fig.colorbar(contour_fill, ax=ax, label='Potencial Elétrico (V)') # Adiciona barra de cores

        # Contour para linhas equipotenciais
        ax.contour(X, Y, potential, levels=20, colors='white', linewidths=0.7, alpha=0.8)
        
        # Streamplot para linhas de campo
        ax.streamplot(X, Y, Ex_norm, Ey_norm, color='black', linewidth=0.8, density=1.8, arrowstyle='->', arrowsize=1.0)
        
        # Plotar as cargas
        charge_colors = ['red' if q[2] > 0 else 'blue' for q in charges] # Cores baseadas no sinal da carga
        ax.scatter(charges[:, 0], charges[:, 1], c=charge_colors,
                   s=np.abs(charges[:, 2]) * 1e11, # Tamanho proporcional à magnitude da carga (ajustar multiplicador)
                   edgecolors='black', zorder=5,  alpha=0.9)
        
        ax.set_title(f'Campo e Potencial Elétrico', fontsize=14)
        ax.set_xlabel('X (m)', fontsize=12)
        ax.set_ylabel('Y (m)', fontsize=12)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect('equal', adjustable='box') # Mantém a proporção correta
        ax.grid(True, linestyle='--', alpha=0.6)

    # Tenta criar a animação
    try:
        ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=150) # interval em ms
        fig.patch.set_facecolor('#fff8dc')  # Define fundo da figura
        ani.save(gif_path, writer=PillowWriter(fps=3), dpi=100)

    except Exception as e:
        print(f"Erro ao gerar animação: {e}")
       
    finally:
        plt.close(fig) # Fundamental para liberar memória

    if os.path.exists(gif_path):
        return send_file(gif_path, mimetype='image/gif', as_attachment=False, download_name='simulacao.gif')
    else:
        return "Erro: arquivo GIF não encontrado após tentativa de geração.", 404


if __name__ == '__main__':
    print("Iniciando...321")
    app.run(debug=True)