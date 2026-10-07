import os
import sys
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = r"c:\Users\Sebas\OneDrive\Documents\Sergio Arboleda\Trabajos\Sistemas operativos\Taller - IA nube e IA local - Sistemas Operativos"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "Screenshots")
PDF_PATH = os.path.join(BASE_DIR, "Informe_Taller_IA_Local_Sistemas_Operativos.pdf")

STUDENTS = "Estudiantes: ANDRÉS SEBASTIÁN CORAL VALLEJO, JUAN ORJUELA, JAVIER ROSERO, ANGEL ARCOS"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D")) # Navy
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "UNIVERSIDAD SERGIO ARBOLEDA — SISTEMAS OPERATIVOS")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#4A5568"))
            self.drawRightString(letter[0] - 54, letter[1] - 36, "Laboratorio IA Local: Ubuntu + Ollama")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 46, letter[0] - 54, 46)
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E293B"))
        self.drawString(54, 34, STUDENTS)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom palette
    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_accent = colors.HexColor("#2563EB")     # Blue 600
    c_secondary = colors.HexColor("#334155")  # Slate 700
    c_light_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_border = colors.HexColor("#E2E8F0")     # Slate 200

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_accent,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Header3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_secondary,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderPadding=5,
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'MetaBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_secondary,
        alignment=1
    )

    tbl_head = ParagraphStyle('TblHead', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white, alignment=1)
    tbl_cell = ParagraphStyle('TblCell', fontName='Helvetica', fontSize=8, leading=10.5, textColor=c_secondary)
    tbl_cell_bold = ParagraphStyle('TblCellB', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=c_primary)

    story = []

    # ========================== PORTADA ==========================
    story.append(Spacer(1, 15))
    story.append(Paragraph("UNIVERSIDAD SERGIO ARBOLEDA", subtitle_style))
    story.append(Paragraph("ESCUELA DE CIENCIAS EXACTAS E INGENIERÍA", ParagraphStyle('Sub', parent=subtitle_style, fontSize=11, textColor=colors.HexColor("#64748B"))))
    story.append(Paragraph("DEPARTAMENTO DE SISTEMAS Y TELECOMUNICACIONES", ParagraphStyle('Sub2', parent=subtitle_style, fontSize=10, textColor=colors.HexColor("#64748B"))))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=0, spaceAfter=20))
    
    story.append(Paragraph("TALLER PRÁCTICO DE SISTEMAS OPERATIVOS", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Despliegue y Administración de Inteligencia Artificial Local (Ubuntu VM + Ollama)", title_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<i>Estudio del Comportamiento del Sistema Operativo en la Virtualización, Gestión de Servicios con Systemd, Recursos del Kernel e Inferencia Local</i>", ParagraphStyle('Ital', parent=title_style, fontName='Helvetica-Oblique', fontSize=10.5, leading=14, textColor=colors.HexColor("#475569"))))
    
    story.append(Spacer(1, 25))
    
    info_data = [
        [Paragraph("<b>Docente:</b>", tbl_cell_bold), Paragraph("Mg. Iván Darío Méndez Aguilera · <i>Hacker Vista Negra</i>", tbl_cell)],
        [Paragraph("<b>Asignatura:</b>", tbl_cell_bold), Paragraph("Sistemas Operativos (Laboratorio Práctico)", tbl_cell)],
        [Paragraph("<b>Estudiantes:</b>", tbl_cell_bold), Paragraph("<b>ANDRÉS SEBASTIÁN CORAL VALLEJO<br/>JUAN ORJUELA<br/>JAVIER ROSERO<br/>ANGEL ARCOS</b>", tbl_cell)],
        [Paragraph("<b>Fecha:</b>", tbl_cell_bold), Paragraph("24 de Septiembre de 2026", tbl_cell)],
        [Paragraph("<b>Repositorio GitHub:</b>", tbl_cell_bold), Paragraph("https://github.com/AndresCoral/Taller---IA-nube-e-IA-local---Sistemas-Operativos", tbl_cell)]
    ]
    info_tbl = Table(info_data, colWidths=[110, 390])
    info_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 7),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, c_border)
    ]))
    story.append(info_tbl)

    story.append(Spacer(1, 30))
    notice_text = f"<b>Constancia de Autoría Académica Obligatoria:</b><br/><i>\"{STUDENTS}\"</i><br/>Todas las actividades prácticas de virtualización, diagnóstico de recursos, despliegue de daemon e inferencia de modelos fueron ejecutadas y verificadas directamente en el entorno de laboratorio."
    notice_tbl = Table([[Paragraph(notice_text, meta_style)]], colWidths=[500])
    notice_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(notice_tbl)
    
    story.append(PageBreak())

    # ========================== PARTE 1 ==========================
    story.append(Paragraph("PARTE I: FUNDAMENTOS CONCEPTUALES DE INTELIGENCIA ARTIFICIAL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=12))

    # Punto 1: Definir IA
    story.append(Paragraph("1. Definición Formal de Inteligencia Artificial (IA)", h2_style))
    story.append(Paragraph(
        "Desde la perspectiva de las Ciencias de la Computación y la Ingeniería de Sistemas, la <b>Inteligencia Artificial (IA)</b> es la disciplina científica y tecnológica dedicada al diseño y construcción de sistemas de software y hardware capaces de emular, ejecutar y superar funciones cognitivas comúnmente asociadas a la mente humana. Entre estas funciones se destacan la <b>percepción sensorial</b>, el <b>razonamiento lógico y deductivo</b>, el <b>aprendizaje a partir de datos empíricos</b>, la <b>generalización conceptual</b>, la <b>resolución de problemas complejos</b> y la <b>comprensión semántica del lenguaje natural</b>.",
        body_style
    ))
    story.append(Paragraph(
        "A diferencia del paradigma de programación tradicional (donde un desarrollador codifica explícitamente algoritmos deterministas con reglas lógicas estáticas que transforman entradas en salidas), la Inteligencia Artificial moderna —especialmente a través del <b>Machine Learning (ML)</b> y el <b>Deep Learning (DL)</b>— invierte la ecuación: el sistema recibe grandes volúmenes de datos empíricos y respuestas deseadas, optimizando una función de pérdida mediante algoritmos de descenso de gradiente para inferir automáticamente matrices de parámetros estadísticos (pesos y sesgos) que capturan patrones no lineales de altísima dimensión.",
        body_style
    ))
    story.append(Paragraph("Componentes fundamentales de un sistema moderno de IA:", h3_style))
    story.append(Paragraph("• <b>Datos (Dataset de entrenamiento y validación):</b> La materia prima informativa que define la distribución de probabilidad a modelar.", bullet_style))
    story.append(Paragraph("• <b>Arquitectura del Modelo (Redes Neuronales / Transformers):</b> Estructuras computacionales compuestas por capas de atención multi-cabeza (Multi-Head Attention), normalizaciones y redes feed-forward.", bullet_style))
    story.append(Paragraph("• <b>Infraestructura de Cómputo (CPU, GPU, NPU):</b> Aceleradores de procesamiento masivo en paralelo especializados en operaciones matriciales (GEMM: General Matrix to Matrix Multiplication).", bullet_style))
    story.append(Paragraph("• <b>Motor de Inferencia y Runtime del Sistema Operativo:</b> Capa de software (como llama.cpp u Ollama) que gestiona el cargado en memoria RAM/VRAM, la cuantización (GGUF), la asignación de hilos (threads) y la ejecución de tensores.", bullet_style))

    story.append(Spacer(1, 8))

    # Punto 2: Comparar IA local vs IA nube
    story.append(Paragraph("2. Comparación Exhaustiva: IA Local vs. IA en la Nube", h2_style))
    story.append(Paragraph(
        "La arquitectura del despliegue de modelos de lenguaje determina drásticamente la latencia, la privacidad, la resiliencia operativa y los costos computacionales. A continuación se sintetiza el análisis comparativo técnico entre ambos paradigmas:",
        body_style
    ))

    comp_data = [
        [Paragraph("Criterio Técnico", tbl_head), Paragraph("IA Local (On-Premise / Edge)", tbl_head), Paragraph("IA en la Nube (Cloud APIs)", tbl_head)],
        [
            Paragraph("<b>Privacidad y Soberanía</b>", tbl_cell_bold),
            Paragraph("<b>Máxima y Absoluta.</b> Los datos, prompts y pesos nunca abandonan la memoria RAM/VRAM ni el almacenamiento del equipo. Cumple estrictamente con regulaciones como GDPR, HIPAA y normativas de secreto bancario/industrial.", tbl_cell),
            Paragraph("<b>Compartida / Tercerizada.</b> La información transita redes WAN públicas y se procesa en datacenters de proveedores (OpenAI, Anthropic, Google), sujeta a términos de servicio, telemetría y riesgos de filtración.", tbl_cell)
        ],
        [
            Paragraph("<b>Latencia y Tiempo de Respuesta</b>", tbl_cell_bold),
            Paragraph("<b>Latencia de Red Cero (0 ms RTT).</b> La respuesta inicial (Time to First Token - TTFT) depende exclusivamente del ancho de banda del bus de memoria local (DDR5 / VRAM) y de la potencia de la CPU/GPU.", tbl_cell),
            Paragraph("<b>Dependiente de Conexión WAN.</b> Sujeta a fluctuaciones de enrutamiento de Internet (RTT ~50-250 ms), congestión de colas en los clústeres del proveedor y políticas de rate limiting.", tbl_cell)
        ],
        [
            Paragraph("<b>Estructura de Costos</b>", tbl_cell_bold),
            Paragraph("<b>Capex Fijo, Opex Mínimo.</b> Se invierte en el hardware existente. El costo marginal por millón de tokens generados es prácticamente $0 (únicamente el consumo de energía eléctrica del PC).", tbl_cell),
            Paragraph("<b>Opex Variable Recurrente.</b> Facturación por token entrante/saliente o suscripción mensual. En proyectos de alta demanda o consultas masivas, los costos escalan exponencialmente.", tbl_cell)
        ],
        [
            Paragraph("<b>Disponibilidad y Dependencia</b>", tbl_cell_bold),
            Paragraph("<b>100% Autónomo y Offline.</b> Funciona sin conexión a Internet. Esencial para infraestructura crítica, operaciones militares, entornos aislados (air-gapped) o redes industriales SCADA.", tbl_cell),
            Paragraph("<b>Dependencia Crítica de Conectividad.</b> Si la conexión WAN falla o la infraestructura cloud experimenta una interrupción (outage), el servicio de IA se interrumpe por completo.", tbl_cell)
        ],
        [
            Paragraph("<b>Escala y Tamaño de Modelos</b>", tbl_cell_bold),
            Paragraph("<b>Acotada al Hardware Local.</b> Limitada a modelos de 0.5B hasta 14B parámetros en equipos personales con 16-32 GB de RAM. Modelos densos de 70B+ requieren workstations multi-GPU.", tbl_cell),
            Paragraph("<b>Modelos Frontera Masivos.</b> Capacidad de ejecutar modelos de cientos de miles de millones de parámetros (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro) alojados en superclústeres H100.", tbl_cell)
        ],
        [
            Paragraph("<b>Control y Personalización</b>", tbl_cell_bold),
            Paragraph("<b>Control Total del Stack.</b> Libertad absoluta para definir <i>Modelfile</i>, temperatura, ventana de contexto, quantización personalizada y prompts sin filtros o censuras externas arbitrarias.", tbl_cell),
            Paragraph("<b>Caja Negra con Filtros.</b> Parámetros restringidos a la API del proveedor. Los modelos pueden ser deprecados, alterados en comportamiento o retirados sin previo aviso.", tbl_cell)
        ]
    ]

    comp_tbl = Table(comp_data, colWidths=[100, 200, 200])
    comp_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg])
    ]))
    story.append(comp_tbl)

    story.append(Spacer(1, 10))

    # Punto 3: 5 Modelos viables en el PC
    story.append(Paragraph("3. Selección de 5 Modelos de IA Viables para el Hardware del PC Anfitrión", h2_style))
    story.append(Paragraph(
        "<b>Auditoría del Hardware Físico del Equipo Anfitrión:</b><br/>"
        "• <b>Procesador (CPU):</b> AMD Ryzen 7 260 con arquitectura Zen 4, 8 núcleos físicos y 16 hilos de procesamiento (hasta 5.1 GHz).<br/>"
        "• <b>Memoria del Sistema (RAM):</b> 16 GB DDR5 a alta velocidad (ancho de banda superior a 5600 MT/s).<br/>"
        "• <b>Tarjeta Gráfica Dedicada (GPU):</b> NVIDIA GeForce RTX 5050 Laptop GPU con 4 GB de VRAM GDDR6/GDDR7 dedicada + AMD Radeon 780M (iGPU integrada con soporte RDNA 3).<br/>"
        "• <b>Almacenamiento:</b> Unidad de estado sólido NVMe PCIe 4.0 con más de 580 GB de espacio libre disponible.",
        body_style
    ))
    story.append(Paragraph(
        "Considerando el presupuesto térmico y de memoria (4 GB de VRAM en la GPU NVIDIA y 16 GB de RAM del sistema), los 5 modelos de IA de pesos abiertos más óptimos y recomendados para este equipo son:",
        body_style
    ))

    p3_data = [
        [Paragraph("Modelo y Versión", tbl_head), Paragraph("Parámetros y Peso", tbl_head), Paragraph("Requisitos de Memoria", tbl_head), Paragraph("Justificación Técnica en el PC Anfitrión", tbl_head)],
        [
            Paragraph("<b>1. Llama 3.2 (1B / 3B)</b><br/><i>Meta AI</i>", tbl_cell_bold),
            Paragraph("1.23B (~1.3 GB)<br/>3.21B (~2.0 GB Q4)", tbl_cell),
            Paragraph("1.5 GB VRAM (1B)<br/>3.2 GB VRAM (3B)", tbl_cell),
            Paragraph("El modelo de 1B cabe íntegramente en los 4 GB de VRAM de la RTX 5050, alcanzando tasas superiores a 60 tokens/segundo. El modelo de 3B cuantizado a 4 bits (Q4_K_M) opera totalmente acelerado por Tensor Cores con ventana de contexto de hasta 8K tokens.", tbl_cell)
        ],
        [
            Paragraph("<b>2. Qwen 2.5 (1.5B / 3B)</b><br/><i>Alibaba Cloud</i>", tbl_cell_bold),
            Paragraph("1.54B (~1.2 GB)<br/>3.09B (~2.2 GB Q4)", tbl_cell),
            Paragraph("1.8 GB VRAM (1.5B)<br/>3.5 GB VRAM (3B)", tbl_cell),
            Paragraph("Considerado el estado del arte en Small Language Models (SLMs). Destaca en razonamiento matemático, generación de código y seguimiento estricto de formato JSON. Se ejecuta a máxima velocidad en la RTX 5050.", tbl_cell)
        ],
        [
            Paragraph("<b>3. Phi-3.5 Mini / Phi-4-mini</b><br/><i>Microsoft Research</i>", tbl_cell_bold),
            Paragraph("3.82B (~2.3 GB Q4)", tbl_cell),
            Paragraph("3.2 GB VRAM", tbl_cell),
            Paragraph("Entrenado intensivamente con datos sintéticos de alta densidad lógica ('textbooks quality'). Su formato cuantizado a Q4_K_M encaja perfecto en los 4 GB de VRAM, permitiendo razonamiento deductivo complejo sin consumir RAM del sistema.", tbl_cell)
        ],
        [
            Paragraph("<b>4. Gemma 2 (2B)</b><br/><i>Google DeepMind</i>", tbl_cell_bold),
            Paragraph("2.61B (~1.6 GB Q4)", tbl_cell),
            Paragraph("2.4 GB VRAM", tbl_cell),
            Paragraph("Arquitectura moderna con atención deslizante local/global (sliding window attention). Entrega una precisión conversacional excepcional superando a modelos del doble de su tamaño. Velocidad de inferencia instantánea en GPU.", tbl_cell)
        ],
        [
            Paragraph("<b>5. DeepSeek-R1-Distill-Qwen-1.5B</b><br/><i>DeepSeek AI</i>", tbl_cell_bold),
            Paragraph("1.5B (~1.1 GB Q4)", tbl_cell),
            Paragraph("1.6 GB VRAM", tbl_cell),
            Paragraph("Especializado en razonamiento formal (Chain of Thought - CoT). El modelo genera trazas explícitas de pensamiento paso a paso antes de emitir conclusiones técnicas. Al requerir solo 1.6 GB de VRAM, corre con fluidez absoluta en la RTX 5050.", tbl_cell)
        ]
    ]

    p3_tbl = Table(p3_data, colWidths=[90, 85, 85, 240])
    p3_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg])
    ]))
    story.append(p3_tbl)

    story.append(Spacer(1, 10))

    # Punto 4: Tipos de IA local y viabilidad
    story.append(Paragraph("4. Taxonomía de Tipos de IA Local y Viabilidad en el PC", h2_style))
    story.append(Paragraph(
        "En el ecosistema computacional actual, la Inteligencia Artificial local abarca diversas familias arquitectónicas especializadas en modalidades sensoriales distintas. A continuación se analiza qué tipos puede ejecutar el equipo del estudiante:",
        body_style
    ))

    p4_data = [
        [Paragraph("Familia de IA Local", tbl_head), Paragraph("Función Principal y Ejemplos", tbl_head), Paragraph("Requisitos Típicos", tbl_head), Paragraph("¿Viable en mi PC?", tbl_head)],
        [
            Paragraph("<b>LLMs / SLMs (Modelos de Lenguaje)</b>", tbl_cell_bold),
            Paragraph("Generación de texto, asistencia técnica, resumen, programación (Qwen 2.5, Llama 3.2, Phi-3.5, Mistral).", tbl_cell),
            Paragraph("1 GB a 6 GB VRAM / RAM según cuantización (Q4/Q8).", tbl_cell),
            Paragraph("<b>100% VIABLE.</b> Modelos de 1B a 3.8B corren en los 4GB de VRAM. Modelos de 7B/8B corren en modo híbrido (GPU offload + RAM DDR5).", tbl_cell)
        ],
        [
            Paragraph("<b>Modelos de Embeddings (Vectores)</b>", tbl_cell_bold),
            Paragraph("Representación matemática de texto para búsqueda semántica y RAG (nomic-embed-text, bge-small).", tbl_cell),
            Paragraph("200 MB a 600 MB RAM/VRAM.", tbl_cell),
            Paragraph("<b>100% VIABLE.</b> Consumo despreciable de recursos. Se ejecutan con latencias inferiores a 5 milisegundos por párrafo.", tbl_cell)
        ],
        [
            Paragraph("<b>Modelos de Audio (ASR / TTS)</b>", tbl_cell_bold),
            Paragraph("Transcripción de voz a texto (OpenAI Whisper) y síntesis de voz hiperrealista (Piper, Kokoro, Bark).", tbl_cell),
            Paragraph("500 MB a 3 GB VRAM para Whisper Tiny/Base/Small.", tbl_cell),
            Paragraph("<b>100% VIABLE.</b> Whisper 'small' o 'medium' cuantizado transcribe audios en tiempo real en la RTX 5050 con CUDA.", tbl_cell)
        ],
        [
            Paragraph("<b>Modelos de Visión (VLM)</b>", tbl_cell_bold),
            Paragraph("Comprensión visual y OCR contextual de imágenes (Moondream 2, MiniCPM-V 2.6).", tbl_cell),
            Paragraph("2.5 GB a 4 GB VRAM.", tbl_cell),
            Paragraph("<b>VIABLE (Modelos Compactos).</b> Moondream2 (~1.8B) cabe completo en la RTX 5050. Llama-3.2-Vision (11B) requiere CPU offload.", tbl_cell)
        ],
        [
            Paragraph("<b>Modelos de Difusión (Imágenes)</b>", tbl_cell_bold),
            Paragraph("Generación sintética de imágenes a partir de texto (Stable Diffusion 1.5, SDXL-Turbo, Flux-schnell).", tbl_cell),
            Paragraph("4 GB a 8 GB VRAM (con cuantización NF4 o INT8).", tbl_cell),
            Paragraph("<b>VIABLE (SD 1.5 / SDXL Turbo).</b> Con técnicas de atención optimizadas (xFormers / FlashAttention) y podado FP16.", tbl_cell)
        ]
    ]

    p4_tbl = Table(p4_data, colWidths=[100, 150, 110, 140])
    p4_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg])
    ]))
    story.append(p4_tbl)

    story.append(PageBreak())

    # ========================== PARTE 2: SECCIÓN 02 ==========================
    story.append(Paragraph("PARTE II: PREPARACIÓN DE LA MÁQUINA VIRTUAL UBUNTU (SECCIÓN 02)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=12))

    story.append(Paragraph("1. Dimensionamiento y Configuración de Recursos en VirtualBox", h2_style))
    story.append(Paragraph(
        "Para garantizar un aislamiento riguroso del sistema anfitrión Windows y evitar contaminar el entorno de desarrollo principal, se procedió a crear una máquina virtual dedicada con <b>Ubuntu 24.04 LTS (Noble Numbat)</b> en Oracle VirtualBox 7.2.14. Se dimensionaron los recursos cumpliendo las especificaciones del taller:",
        body_style
    ))
    story.append(Paragraph("• <b>Procesadores virtuales (vCPU):</b> 4 núcleos asignados (de los 16 hilos disponibles en el AMD Ryzen 7 260).", bullet_style))
    story.append(Paragraph("• <b>Memoria RAM de la VM:</b> 8192 MB (8.0 GB) asignados de los 16 GB físicos del equipo anfitrión.", bullet_style))
    story.append(Paragraph("• <b>Almacenamiento Virtual:</b> Disco virtual dinámico redimensionado a 50 GB (VDI) conectado a controladora SCSI LsiLogic, con partición raíz de 49 GB.", bullet_style))
    story.append(Paragraph("• <b>Configuración de Red:</b> Modo NAT con reenvío de puertos (Port Forwarding): <code>2222 -> 22</code> (SSH) y <code>11434 -> 11434</code> (Ollama REST API).", bullet_style))
    story.append(Paragraph("• <b>Snapshot de Seguridad:</b> Se generó el punto de restauración <code>Snapshot-Inicial-PreOllama</code> previo a cualquier modificación de paquetes.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Análisis de Sobreasignación de Recursos (Overcommit y Swapping)", h3_style))
    story.append(Paragraph(
        "<b>¿Qué ocurre si se asigna demasiada RAM o demasiadas vCPU a una máquina virtual?</b><br/>"
        "1. <b>Sobreasignación de Memoria (Memory Overcommit):</b> Si la máquina virtual reclama más memoria de la que el sistema operativo anfitrión (Host) tiene físicamente libre, el kernel de Windows se ve forzado a realizar <i>paginación en disco</i> (Paging/Thrashing). Esto degrada el rendimiento de todo el computador, provocando bloqueos del hipervisor y activando potencialmente el <i>OOM Killer</i> (Out-Of-Memory) de Linux dentro de la VM.<br/>"
        "2. <b>Sobreasignación de CPU (vCPU Overcommit):</b> Si se asignan más vCPUs que hilos físicos disponibles (o todos los hilos), el planificador de la CPU del Host (Scheduler) sufre una sobrecarga masiva por cambios de contexto constantes (Context Switching Latency) y tiempos de espera de sincronización en el hipervisor (CPU Co-scheduling wait time), ralentizando tanto a la VM como a los procesos del anfitrión.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Evidencias de Verificación del Sistema Operativo en la VM", h2_style))

    # Screenshot Sec02_01
    shot1_path = os.path.join(SCREENSHOTS_DIR, "Sec02_01_CPU_RAM.png")
    if os.path.exists(shot1_path):
        story.append(Paragraph("<b>Figura 2.1:</b> Verificación de Kernel, vCPU y Memoria RAM asignada (<code>uname -a</code>, <code>nproc</code>, <code>free -h</code>, <code>lscpu</code>)", h3_style))
        story.append(Image(shot1_path, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 8))

    # Screenshot Sec02_02
    shot2_path = os.path.join(SCREENSHOTS_DIR, "Sec02_02_Disco_SistemaArchivos.png")
    if os.path.exists(shot2_path):
        story.append(Paragraph("<b>Figura 2.2:</b> Verificación de Discos, Bloques y Espacio en Sistema de Archivos (<code>lsblk</code>, <code>df -h</code>, <code>du -sh</code>)", h3_style))
        story.append(Image(shot2_path, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ========================== PARTE 3: SECCIÓN 03 ==========================
    story.append(Paragraph("PARTE III: INSTALACIÓN Y VERIFICACIÓN DE OLLAMA (SECCIÓN 03)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=12))

    story.append(Paragraph("1. Proceso de Actualización e Instalación del Daemon", h2_style))
    story.append(Paragraph(
        "Dentro de la máquina virtual Ubuntu, se procedió a actualizar los repositorios oficiales mediante el gestor de paquetes <code>apt</code> y a desplegar las utilidades esenciales de diagnóstico (<code>curl</code>, <code>wget</code>, <code>git</code>, <code>pciutils</code>, <code>lshw</code>, <code>htop</code>, <code>net-tools</code>). Posteriormente se ejecutó el instalador oficial de Ollama para arquitecturas Linux x86_64:",
        body_style
    ))
    story.append(Paragraph("<code>curl -fsSL https://ollama.com/install.sh | sh</code>", code_style))
    story.append(Paragraph(
        "El instalador descargó el binario optimizado en <code>/usr/local/bin/ollama</code>, creó un usuario de sistema dedicado sin privilegios de shell (<code>ollama</code>) asignado a los grupos <code>render</code> y <code>video</code>, y generó automáticamente la unidad de servicio de systemd en <code>/etc/systemd/system/ollama.service</code>.",
        body_style
    ))

    # Screenshot Sec03_02
    shot_inst = os.path.join(SCREENSHOTS_DIR, "Sec03_02_Instalacion_Ollama.png")
    if os.path.exists(shot_inst):
        story.append(Paragraph("<b>Figura 3.1:</b> Ejecución del instalador oficial de Ollama y creación de la unidad de systemd", h3_style))
        story.append(Image(shot_inst, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 8))

    # Screenshot Sec03_03
    shot_serv = os.path.join(SCREENSHOTS_DIR, "Sec03_03_Servicio_API_Tags.png")
    if os.path.exists(shot_serv):
        story.append(Paragraph("<b>Figura 3.2:</b> Habilitación del servicio con <code>systemctl enable --now ollama</code> y verificación del endpoint local <code>/api/tags</code>", h3_style))
        story.append(Image(shot_serv, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ========================== PARTE 4: SECCIÓN 04 ==========================
    story.append(Paragraph("PARTE IV: ADMINISTRACIÓN DE OLLAMA EN UBUNTU (SECCIÓN 04)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=12))

    story.append(Paragraph("1. Control de Ciclo de Vida del Servicio y Superficie de Red", h2_style))
    story.append(Paragraph(
        "En un sistema operativo Linux de nivel de producción, los demonios de inferencia deben ser administrados mediante <b>systemd</b> para asegurar reinicios automáticos ante fallas, aislamiento de cgroups y control de recursos. Se ejecutaron pruebas de reinicio de la unidad (<code>systemctl restart ollama</code>) y consulta de logs en tiempo real mediante <code>journalctl -u ollama</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Auditoría de Red y Sockets:</b> Mediante el comando <code>ss -lntp | grep 11434</code> se comprobó que el servicio escucha exclusivamente en la dirección loopback <code>127.0.0.1:11434</code>. Esta configuración es vital para la seguridad: evita que equipos externos en la misma red local puedan enviar consultas sin autenticación a la API de inferencia, restringiendo el acceso exclusivamente a los clientes autorizados en el host.",
        body_style
    ))

    # Screenshot Sec04_01
    shot_sec4_1 = os.path.join(SCREENSHOTS_DIR, "Sec04_01_Servicio_Restart_Logs.png")
    if os.path.exists(shot_sec4_1):
        story.append(Paragraph("<b>Figura 4.1:</b> Reinicio del daemon y consulta de logs estructurados con <code>journalctl</code>", h3_style))
        story.append(Image(shot_sec4_1, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Screenshot Sec04_02
    shot_sec4_2 = os.path.join(SCREENSHOTS_DIR, "Sec04_02_Red_Puerto11434.png")
    if os.path.exists(shot_sec4_2):
        story.append(Paragraph("<b>Figura 4.2:</b> Verificación del socket de escucha TCP en puerto 11434 y consulta con curl", h3_style))
        story.append(Image(shot_sec4_2, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("2. Medición de Consumo de RAM en Reposo (Línea Base)", h2_style))
    story.append(Paragraph(
        "Previo a la descarga y ejecución de cualquier modelo, se registró la huella de memoria RAM del sistema operativo en estado de reposo (Idle Baseline):<br/>"
        "• <b>Memoria Total de la VM:</b> 7.8 GiB.<br/>"
        "• <b>Memoria Usada en Reposo:</b> 498 MiB (incluyendo kernel, systemd y servicios de red).<br/>"
        "• <b>Consumo del Daemon de Ollama:</b> PID 2923 consumiendo únicamente 34.9 MB de memoria residente (RSS) y 0.4% de la RAM total, confirmando la eficiencia del servicio mientras espera peticiones HTTP.",
        body_style
    ))

    # Screenshot Sec04_03
    shot_sec4_3 = os.path.join(SCREENSHOTS_DIR, "Sec04_03_Recursos_Reposo.png")
    if os.path.exists(shot_sec4_3):
        story.append(Paragraph("<b>Figura 4.3:</b> Medición del consumo de memoria en reposo y proceso <code>ollama serve</code> antes de cargar modelos", h3_style))
        story.append(Image(shot_sec4_3, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ========================== PARTE 5: SECCIÓN 05 ==========================
    story.append(Paragraph("PARTE V: DESCARGA, EJECUCIÓN Y ADMINISTRACIÓN DE MODELOS (SECCIÓN 05)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=2, spaceAfter=12))

    story.append(Paragraph("1. Evaluación y Comparación Técnica de Modelos en la VM", h2_style))
    story.append(Paragraph(
        "Cumpliendo el objetivo central de la Sección 05 del taller, se descargaron, ejecutaron y administraron tres modelos de IA oficiales con diferentes arquitecturas y escalas. A cada modelo se le formuló exactamente la misma consulta técnica de Sistemas Operativos: <i>\"¿Qué es un sistema operativo? Responde brevemente.\"</i>, evaluando tiempos, memoria RAM asignada en tiempo real (<code>ollama ps</code>) y calidad de la respuesta.",
        body_style
    ))

    # Tabla comparativa de la sección 05
    res_data = [
        [Paragraph("Modelo Evaluado", tbl_head), Paragraph("Tamaño Disco", tbl_head), Paragraph("RAM Ocupada", tbl_head), Paragraph("Tiempo Inferencia", tbl_head), Paragraph("¿Funciona?", tbl_head), Paragraph("Calidad / Observación Técnica", tbl_head)],
        [
            Paragraph("<b>smollm2:135m</b><br/><i>HuggingFace</i>", tbl_cell_bold),
            Paragraph("270 MB (GGUF)", tbl_cell),
            Paragraph("382 MB (en RAM)", tbl_cell),
            Paragraph("~0.8 s (Ultrarrápido)", tbl_cell),
            Paragraph("<font color='#16A34A'><b>SÍ</b></font>", tbl_cell_bold),
            Paragraph("Excelente velocidad. Definición concisa y coherente con gramática estructurada adecuada para su tamaño diminuto.", tbl_cell)
        ],
        [
            Paragraph("<b>qwen2.5:0.5b</b><br/><i>Alibaba</i>", tbl_cell_bold),
            Paragraph("397 MB (GGUF)", tbl_cell),
            Paragraph("512 MB (en RAM)", tbl_cell),
            Paragraph("~1.2 s (Muy Rápido)", tbl_cell),
            Paragraph("<font color='#16A34A'><b>SÍ</b></font>", tbl_cell_bold),
            Paragraph("Precisión conceptual sobresaliente en español. Explica el rol de intermediario entre hardware y aplicaciones a la perfección.", tbl_cell)
        ],
        [
            Paragraph("<b>tinyllama:latest</b><br/><i>1.1B Llama-arch</i>", tbl_cell_bold),
            Paragraph("637 MB (GGUF)", tbl_cell),
            Paragraph("840 MB (en RAM)", tbl_cell),
            Paragraph("~2.5 s (Rápido)", tbl_cell),
            Paragraph("<font color='#16A34A'><b>SÍ</b></font>", tbl_cell_bold),
            Paragraph("Definición completa cubriendo administración de recursos, procesos y memoria. Mayor profundidad argumentativa.", tbl_cell)
        ]
    ]

    res_tbl = Table(res_data, colWidths=[95, 75, 75, 80, 55, 120])
    res_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg])
    ]))
    story.append(res_tbl)

    story.append(Spacer(1, 10))

    # Screenshots de la sección 05
    story.append(Paragraph("2. Evidencias Fotográficas de Descarga e Inferencia", h2_style))

    # Sec05_01
    shot5_1 = os.path.join(SCREENSHOTS_DIR, "Sec05_01_Pull_SmolLM2.png")
    if os.path.exists(shot5_1):
        story.append(Paragraph("<b>Figura 5.1:</b> Descarga de modelo con <code>ollama pull smollm2:135m</code> y verificación en <code>ollama list</code>", h3_style))
        story.append(Image(shot5_1, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Sec05_02
    shot5_2 = os.path.join(SCREENSHOTS_DIR, "Sec05_02_Run_SmolLM2_PS.png")
    if os.path.exists(shot5_2):
        story.append(Paragraph("<b>Figura 5.2:</b> Inferencia y monitoreo en memoria con <code>ollama ps</code> y <code>free -h</code> para smollm2:135m", h3_style))
        story.append(Image(shot5_2, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Sec05_03
    shot5_3 = os.path.join(SCREENSHOTS_DIR, "Sec05_03_Pull_Qwen.png")
    if os.path.exists(shot5_3):
        story.append(Paragraph("<b>Figura 5.3:</b> Descarga y verificación de qwen2.5:0.5b", h3_style))
        story.append(Image(shot5_3, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Sec05_04
    shot5_4 = os.path.join(SCREENSHOTS_DIR, "Sec05_04_Run_Qwen_PS.png")
    if os.path.exists(shot5_4):
        story.append(Paragraph("<b>Figura 5.4:</b> Inferencia y monitoreo de qwen2.5:0.5b cargado en RAM de la VM", h3_style))
        story.append(Image(shot5_4, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Sec05_05
    shot5_5 = os.path.join(SCREENSHOTS_DIR, "Sec05_05_Pull_TinyLlama.png")
    if os.path.exists(shot5_5):
        story.append(Paragraph("<b>Figura 5.5:</b> Descarga de modelo tinyllama (1.1B parámetros)", h3_style))
        story.append(Image(shot5_5, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Sec05_06
    shot5_6 = os.path.join(SCREENSHOTS_DIR, "Sec05_06_Run_TinyLlama_PS.png")
    if os.path.exists(shot5_6):
        story.append(Paragraph("<b>Figura 5.6:</b> Inferencia de tinyllama y validación de recursos de CPU y RAM ocupada", h3_style))
        story.append(Image(shot5_6, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    # Sec05_07
    shot5_7 = os.path.join(SCREENSHOTS_DIR, "Sec05_07_Admin_Show_CP_Stop_RM.png")
    if os.path.exists(shot5_7):
        story.append(Paragraph("<b>Figura 5.7:</b> Administración completa de modelos: <code>ollama show</code>, creación de copias/alias con <code>ollama cp</code>, detención de procesos en memoria con <code>ollama stop</code> y eliminación con <code>ollama rm</code>", h3_style))
        story.append(Image(shot5_7, width=6.5*inch, height=3.65*inch))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Conclusiones Técnicas de la Sección 05", h2_style))
    story.append(Paragraph(
        "1. <b>El Sistema Operativo como Gestor de Carga:</b> Se demostró que la inferencia de Inteligencia Artificial es una carga intensiva de memoria y cómputo que el kernel de Linux administra con alta fidelidad a través de paginación y asignación de hilos. En modo CPU-only dentro de la VM, los 4 vCPUs asignados permitieron tiempos de respuesta rápidos y fluidos en modelos compactos.<br/>"
        "2. <b>Eficiencia del Ciclo de Vida con Ollama:</b> El daemon de Ollama implementa una gestión inteligente de memoria RAM: al terminar una consulta, el modelo permanece cargado durante un temporizador de inactividad (<i>keep-alive</i> de 5 minutos por defecto) para acelerar consultas subsecuentes sin re-lectura de disco; sin embargo, al invocar <code>ollama stop</code>, la memoria se libera de inmediato hacia el buffer/cache del sistema operativo.<br/>"
        "3. <b>Estado del Entorno:</b> El taller ha alcanzado la culminación rigurosa de la <b>Sección 05</b> conforme a las directrices de la guía académica, dejando el entorno virtualizado de Ubuntu y los servicios de IA perfectamente configurados y listos para la siguiente fase de desarrollo (Sección 06: Modelfile, API y Frontend).",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {PDF_PATH}")
    return PDF_PATH

if __name__ == "__main__":
    print(STUDENTS)
    build_pdf()
    print(STUDENTS)
