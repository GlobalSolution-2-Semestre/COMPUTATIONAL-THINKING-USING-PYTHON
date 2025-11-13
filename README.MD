# MindTrack - Plataforma de Bem-Estar (Global Solution)

Este projeto foi desenvolvido para a Global Solution de **Computational Thinking Using Python** da FIAP. É uma aplicação de console que se conecta a um banco de dados Oracle para realizar operações de CRUD (Create, Read, Update, Delete) e consultas relacionadas ao bem-estar e saúde mental dos colaboradores.

## 👩‍💻 Integrantes

* **Nome:** Guilherme Macedo Martins | **RM:** 562396 | **Turma:** 1TDSPF
* **Nome:** Pedro Henrique Luiz Alves Duarte | **RM:** 563405 | **Turma:** 1TDSPF

---

## 🚀 Instruções de Instalação e Execução

Este guia contém as instruções detalhadas para a instalação de complementos externos e a execução do sistema, conforme solicitado nos requisitos do projeto.

### 1. Requisitos do Sistema

* **Python 3.7+** instalado em sua máquina.
* **Acesso à rede da FIAP** (seja presencialmente ou via VPN), pois o banco de dados (`oracle.com.fiap`) é acessível apenas internamente.

### 2. Instalação de Complementos Externos

O projeto necessita de **uma biblioteca externa** que não faz parte da instalação padrão do Python: `oracledb`.
Esta biblioteca é o driver oficial da Oracle que permite ao Python se comunicar com o banco de dados.
Para instalá-la, abra seu terminal (Prompt de Comando, PowerShell ou Terminal) e execute o seguinte comando:

```bash
pip install oracledb