
# 📦 SynthNova Physics Simulator EDU — Windows Setup

Simulador de física para robótica basado en MuJoCo, con interfaces de control de alto nivel para el robot Galbot G1.

---

## 📌 Requisitos previos

Antes de instalar este proyecto en tu computador con Windows, asegúrate de tener instalado:

- [Anaconda](https://www.anaconda.com/products/distribution)
- [Git for Windows](https://git-scm.com/downloads)

---

## 📦 Instalación del entorno

### 1️⃣ Clonar este repositorio

Abre **Anaconda Prompt** y ejecuta:

```bash
git clone https://github.com/emersonjleon/physics_sim_edu-1.git
cd physics_sim_edu-1
````

### 2️⃣ Crear entorno Conda desde archivo

Desde la carpeta del proyecto:

```bash
conda env create -f environment.yml
conda activate sim_env
```

---

### 3️⃣ Instalar paquetes locales del proyecto

Con el entorno `sim_env` activado:

```bash
pip install -e ./src/synthnova_config
pip install -e .
```

---

## ✅ Verificar instalación

Desde **Anaconda Prompt**, ejecuta Python y prueba los imports:

```python
from physics_simulator import PhysicsSimulator
from synthnova_config import PhysicsSimulatorConfig

config = PhysicsSimulatorConfig()
sim = PhysicsSimulator(config)
print("Installation successful!")
```

Si ves **Installation successful!**, la instalación fue correcta.
También puedes ejecutar

```bash
cd examples
python basic_usage.py
```
y de forma similar ejecutar los ejemplos de la carpeta `ioai`

---

## 📌 Notas

* Este proyecto requiere **MuJoCo 3.x** configurado en `C:\mujoco`
* Usa **Anaconda Prompt** para todas las operaciones
* Si tienes problemas con MuJoCo, revisa que `C:\mujoco\bin` esté en tu `Path` de variables de entorno

---

## 📚 Créditos

Proyecto basado en el simulador de física MuJoCo, con interfaces desarrolladas para Galbot G1.

## Viejo readme.md


<img src="docs/images/icon.svg" alt="SynthNova Icon" width="40" height="40" style="vertical-align: middle; margin-right: 5px;"> SynthNova Physics Simulator

<div align="right">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a>
</div>

SynthNova Physics Simulator Edu is a robotics simulation framework built on the MuJoCo physics engine for eduactional purposes.

## ⚙️ Installation

```bash
git clone https://github.com/galbot-ioai/physics_sim_edu.git
cd physics_sim_edu
pip install -e ./src/synthnova_config
pip install -e .
```

## 📖 Documentation

Detailed documentation can be found at:

- [Online Documentation](https://galbot-ioai.github.io/physics_sim_edu/)
- [API Reference](https://galbot-ioai.github.io/physics_sim_edu/rsts/api.html)
- [Examples](https://galbot-ioai.github.io/physics_sim_edu/rsts/examples.html)




## 📜 License

```text
Copyright (c) 2023-2025 Galbot. All Rights Reserved.

This software contains confidential and proprietary information of Galbot, Inc.
("Confidential Information"). You shall not disclose such Confidential Information
and shall use it only in accordance with the terms of the license agreement you
entered into with Galbot, Inc.

UNAUTHORIZED COPYING, USE, OR DISTRIBUTION OF THIS SOFTWARE, OR ANY PORTION OR
DERIVATIVE THEREOF, IS STRICTLY PROHIBITED. IF YOU HAVE RECEIVED THIS SOFTWARE IN
ERROR, PLEASE NOTIFY GALBOT, INC. IMMEDIATELY AND DELETE IT FROM YOUR SYSTEM.
```

## mujoco?
- [MuJoCo 3.x](https://mujoco.org/)  
  Descargar y descomprimir en `C:\mujoco`

⚠️ **Configura la variable de entorno MUJOCO_PY_MUJOCO_PATH**:
1. Abre "Configuración avanzada del sistema"
2. Haz clic en "Variables de entorno..."
3. Crea una nueva variable de entorno:
   - Nombre: `MUJOCO_PY_MUJOCO_PATH`
   - Valor: `C:\mujoco`

Agrega también `C:\mujoco\bin` a la variable de entorno `Path`
