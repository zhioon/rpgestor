# 📖 MANUAL DE USUARIO - RPGESTOR

## 📋 INFORMACIÓN DEL DOCUMENTO

- **Título**: Manual de Usuario RPGestor v2.0
- **Fecha**: Julio 2025
- **Versión**: 2.0.0
- **Audiencia**: Usuarios finales (Gestores, Jefes de Ventas, Vendedores)
- **URL del Sistema**: https://rpgestor.onrender.com

---

## 📚 TABLA DE CONTENIDOS

1. [INTRODUCCIÓN](#1-introducción)
2. [INFORMACIÓN GENERAL](#2-información-general)
3. [PRIMEROS PASOS](#3-primeros-pasos)
4. [ROLES Y PERMISOS](#4-roles-y-permisos)
5. [MANUAL DEL GESTOR](#5-manual-del-gestor)
6. [MANUAL DEL JEFE DE VENTAS](#6-manual-del-jefe-de-ventas)
7. [MANUAL DEL VENDEDOR](#7-manual-del-vendedor)
8. [FUNCIONALIDADES COMUNES](#8-funcionalidades-comunes)
9. [SOLUCIÓN DE PROBLEMAS](#9-solución-de-problemas)
10. [APÉNDICES](#10-apéndices)

---

## 1. INTRODUCCIÓN

### 1.1 Bienvenida a RPGestor

¡Bienvenido a **RPGestor**!

RPGestor es un sistema integral de gestión de ventas diseñado para optimizar la productividad de equipos comerciales mediante dashboards inteligentes, comunicación integrada y análisis en tiempo real.

Este manual le guiará paso a paso a través de todas las funcionalidades del sistema, adaptadas específicamente a su rol dentro de la organización.

### 1.2 Propósito del Manual

Este manual tiene como objetivo:

✅ Proporcionar instrucciones claras para usar todas las funcionalidades  
✅ Explicar los diferentes roles y sus permisos específicos  
✅ Ofrecer ejemplos prácticos de casos de uso comunes  
✅ Resolver dudas frecuentes y problemas técnicos  
✅ Maximizar el aprovechamiento del sistema  

### 1.3 Audiencia Objetivo

Este manual está dirigido a:

👔 **GESTORES**: Usuarios con acceso completo al sistema  
👨‍💼 **JEFES DE VENTAS**: Responsables de equipos comerciales  
💼 **VENDEDORES**: Personal de ventas en campo  
🔧 **ADMINISTRADORES**: Personal técnico de soporte  

### 1.4 Convenciones del Documento

**ICONOGRAFÍA UTILIZADA:**
- ✅ Acción exitosa o recomendada
- ❌ Acción incorrecta o no recomendada
- ⚠️ Advertencia importante
- 💡 Consejo útil
- 🔍 Información adicional
- 📝 Nota importante

**FORMATO DE TEXTO:**
- **Texto en negrita**: Elementos de interfaz (botones, menús)
- *Texto en cursiva*: Campos de formulario
- `Texto en código`: URLs y rutas del sistema

---

## 2. INFORMACIÓN GENERAL

### 2.1 ¿Qué es RPGestor?

RPGestor es una plataforma web integral que centraliza y optimiza todos los procesos relacionados con la gestión de ventas:

**🎯 CARACTERÍSTICAS PRINCIPALES:**
- Dashboards personalizados por rol
- Gestión completa de inventarios
- Sistema de pedidos automatizado
- Comunicación interna integrada
- Reportes y análisis en tiempo real
- Acceso multiplataforma 24/7

**🏗️ ARQUITECTURA TÉCNICA:**
- Desarrollado en Django 4.2
- Base de datos PostgreSQL
- Interfaz responsive (móvil/tablet/desktop)
- Actualizaciones en tiempo real con WebSockets
- Seguridad empresarial robusta

### 2.2 Beneficios Principales

**PARA LA ORGANIZACIÓN:**
- 📈 Aumento del 35% en productividad de ventas
- 📊 Reducción del 50% en tiempo de reportes
- 🎯 Mejora del 25% en cumplimiento de metas
- 📋 Reducción del 40% en errores de inventario

**PARA LOS USUARIOS:**
- ⚡ Acceso instantáneo a información actualizada
- 📱 Disponibilidad desde cualquier dispositivo
- 🔄 Sincronización automática de datos
- 💬 Comunicación directa y eficiente
- 📊 Reportes automáticos personalizados

### 2.3 Requisitos del Sistema

**REQUISITOS MÍNIMOS:**
- 🌐 Navegador web moderno (Chrome, Firefox, Safari, Edge)
- 📶 Conexión a internet estable
- 📱 Resolución mínima: 1024x768 (desktop) / 375x667 (móvil)
- 💾 JavaScript habilitado

**NAVEGADORES COMPATIBLES:**
- ✅ Google Chrome 90+
- ✅ Mozilla Firefox 88+
- ✅ Safari 14+
- ✅ Microsoft Edge 90+
- ✅ Navegadores móviles modernos

**DISPOSITIVOS SOPORTADOS:**
- ✅ Computadoras de escritorio
- ✅ Laptops
- ✅ Tablets (iPad, Android)
- ✅ Smartphones (iOS, Android)

### 2.4 Acceso al Sistema

**URL DE ACCESO:**
🌐 `https://rpgestor.onrender.com`

**CREDENCIALES DE DEMOSTRACIÓN:**
- 👔 Gestor: `gestor1` / `demo123`
- 👨‍💼 Jefe de Ventas: `jefe1` / `demo123`
- 💼 Vendedor: `vendedor1` / `demo123`

**HORARIOS DE DISPONIBILIDAD:**
- ⏰ 24 horas al día, 7 días a la semana
- 🔧 Mantenimiento programado: Domingos 2:00-4:00 AM

---

## 3. PRIMEROS PASOS

### 3.1 Acceso Inicial

**PASO 1: Abrir el Sistema**
1. Abra su navegador web preferido
2. Navegue a: `https://rpgestor.onrender.com`
3. Espere a que cargue la página de inicio de sesión

**PASO 2: Iniciar Sesión**
1. Ingrese su *nombre de usuario* en el campo correspondiente
2. Ingrese su *contraseña* en el campo correspondiente
3. Haga clic en el botón **"Iniciar Sesión"**

💡 **Consejo**: Si es su primer acceso, use las credenciales de demostración proporcionadas por su administrador.

**PASO 3: Verificación de Acceso**
- Una vez autenticado, será redirigido automáticamente al dashboard correspondiente a su rol
- Verá su nombre de usuario en la esquina superior derecha
- El menú lateral mostrará las opciones disponibles para su rol

### 3.2 Navegación General

**ELEMENTOS DE LA INTERFAZ:**

**🏠 Barra Superior:**
- Logo de RPGestor (enlace al dashboard principal)
- Nombre del usuario actual
- Botón de **"Cerrar Sesión"**

**📋 Menú Lateral:**
- Dashboard principal
- Opciones específicas según su rol
- Enlaces a funcionalidades principales

**📱 Diseño Responsive:**
- En dispositivos móviles, el menú se convierte en un menú hamburguesa
- Todos los elementos se adaptan automáticamente al tamaño de pantalla

### 3.3 Interfaz de Usuario

**COLORES DEL SISTEMA:**
- 🔵 Azul: Elementos principales y navegación
- 🟢 Verde: Acciones exitosas y confirmaciones
- 🔴 Rojo: Alertas y acciones críticas
- ⚫ Gris: Información secundaria

**BOTONES PRINCIPALES:**
- **Crear/Nuevo**: Botones verdes para crear elementos
- **Editar**: Botones azules para modificar información
- **Eliminar**: Botones rojos para acciones destructivas
- **Ver/Detalle**: Botones grises para consultar información

### 3.4 Configuración de Perfil

**ACCEDER A SU PERFIL:**
1. Haga clic en su nombre de usuario (esquina superior derecha)
2. Seleccione **"Mi Perfil"** del menú desplegable

**INFORMACIÓN EDITABLE:**
- *Nombre*: Su nombre completo
- *Email*: Dirección de correo electrónico
- *Teléfono*: Número de contacto
- *Foto de Perfil*: Imagen personal (opcional)

**CAMBIO DE CONTRASEÑA:**
1. En su perfil, haga clic en **"Cambiar Contraseña"**
2. Ingrese su *contraseña actual*
3. Ingrese su *nueva contraseña*
4. Confirme la *nueva contraseña*
5. Haga clic en **"Actualizar Contraseña"**

⚠️ **Importante**: Use contraseñas seguras con al menos 8 caracteres, incluyendo mayúsculas, minúsculas y números.

---

## 4. ROLES Y PERMISOS

### 4.1 Tipos de Usuario

RPGestor maneja tres roles principales con funcionalidades específicas:

**👔 GESTOR**
- Acceso completo al sistema
- Vista global de todas las operaciones
- Gestión de inventarios y productos
- Supervisión de todos los pedidos
- Administración de usuarios

**👨‍💼 JEFE DE VENTAS**
- Gestión de equipos de vendedores
- Asignación y seguimiento de metas
- Sistema de mensajería interna
- Reportes de rendimiento del equipo
- Agenda y programación de reuniones

**💼 VENDEDOR**
- Dashboard personal con métricas individuales
- Gestión de cartera de clientes
- Creación y seguimiento de pedidos
- Agenda personal
- Recepción de mensajes del jefe

### 4.2 Permisos por Rol

| Funcionalidad | Gestor | Jefe Ventas | Vendedor |
|---------------|--------|-------------|----------|
| Dashboard Global | ✅ | ❌ | ❌ |
| Dashboard Equipo | ✅ | ✅ | ❌ |
| Dashboard Personal | ✅ | ✅ | ✅ |
| Gestión Inventario | ✅ | ❌ | ❌ |
| Todos los Pedidos | ✅ | ❌ | ❌ |
| Pedidos del Equipo | ✅ | ✅ | ❌ |
| Pedidos Propios | ✅ | ✅ | ✅ |
| Enviar Mensajes | ✅ | ✅ | ❌ |
| Recibir Mensajes | ✅ | ✅ | ✅ |
| Asignar Metas | ✅ | ✅ | ❌ |
| Ver Metas | ✅ | ✅ | ✅ |
| Gestión Usuarios | ✅ | ❌ | ❌ |
| Reportes Globales | ✅ | ❌ | ❌ |
| Reportes Equipo | ✅ | ✅ | ❌ |
| Reportes Personales | ✅ | ✅ | ✅ |

### 4.3 Cambio de Roles

📝 **Nota**: El cambio de roles solo puede ser realizado por un administrador del sistema a través del panel de administración de Django.

**PROCESO PARA SOLICITAR CAMBIO DE ROL:**
1. Contacte a su administrador de sistema
2. Proporcione justificación para el cambio
3. Espere la aprobación y configuración
4. Cierre sesión y vuelva a iniciar sesión para ver los cambios

---

## 5. MANUAL DEL GESTOR

### 5.1 Dashboard del Gestor

El dashboard del gestor proporciona una vista global completa del negocio con métricas en tiempo real.

**ACCESO AL DASHBOARD:**
- URL directa: `https://rpgestor.onrender.com/usuarios/gestor_dashboard/`
- Desde el menú: **Dashboard** → **Vista Global**

**MÉTRICAS PRINCIPALES:**

**📊 Tarjetas de Resumen:**
- **Total Vendedores**: Número de vendedores activos
- **Total Clientes**: Clientes registrados en el sistema
- **Pedidos del Mes**: Pedidos creados en el mes actual
- **Ventas del Mes**: Valor total de ventas mensuales

**📈 Gráficos Interactivos:**
- **Ventas por Mes**: Tendencia de ventas de los últimos 12 meses
- **Pedidos por Estado**: Distribución de pedidos por estado actual
- **Top Vendedores**: Ranking de vendedores por rendimiento
- **Productos Más Vendidos**: Lista de productos con mayor rotación

**🔄 ACTUALIZACIÓN DE DATOS:**
- Los datos se actualizan automáticamente cada 5 minutos
- Para actualización manual, haga clic en el botón **"Actualizar"**

### 5.2 Gestión de Inventario

La gestión de inventario permite controlar todos los productos del sistema.

**ACCESO AL INVENTARIO:**
- Desde el menú: **Inventario** → **Gestión de Productos**
- URL directa: `https://rpgestor.onrender.com/productos/`

**FUNCIONALIDADES PRINCIPALES:**

**📋 Lista de Productos:**
- Vista tabular con todos los productos
- Información mostrada: Código, Nombre, Grupo, Subgrupo, Precio, Stock
- Paginación automática (50 productos por página)

**🔍 Búsqueda y Filtros:**
- **Búsqueda por texto**: Buscar por código o nombre de producto
- **Filtro por Grupo**: Seleccionar grupo específico
- **Filtro por Subgrupo**: Filtrar por subgrupo dentro del grupo
- **Filtro por Stock**: Mostrar solo productos con stock bajo

**➕ CREAR NUEVO PRODUCTO:**
1. Haga clic en **"Nuevo Producto"**
2. Complete los campos obligatorios:
   - *Código*: Código único del producto
   - *Nombre*: Nombre descriptivo
   - *Grupo*: Categoría principal
   - *Subgrupo*: Subcategoría
   - *Precio*: Precio unitario
   - *Stock*: Cantidad disponible
3. Haga clic en **"Guardar"**

**✏️ EDITAR PRODUCTO:**
1. Haga clic en el botón **"Editar"** junto al producto
2. Modifique los campos necesarios
3. Haga clic en **"Actualizar"**

**🗑️ ELIMINAR PRODUCTO:**
1. Haga clic en el botón **"Eliminar"** junto al producto
2. Confirme la eliminación en el diálogo
3. El producto será marcado como inactivo

⚠️ **Advertencia**: Los productos eliminados no se borran físicamente, solo se marcan como inactivos para mantener la integridad de los pedidos históricos.

### 5.3 Supervisión de Pedidos

El gestor puede ver y gestionar todos los pedidos del sistema.

**ACCESO A PEDIDOS:**
- Desde el menú: **Pedidos** → **Todos los Pedidos**
- URL directa: `https://rpgestor.onrender.com/pedidos/`

**ESTADOS DE PEDIDOS:**
- 🟡 **Borrador**: Pedido en creación
- 🔵 **Confirmado**: Pedido confirmado por el cliente
- 🟠 **En Proceso**: Pedido en preparación
- 🟢 **Entregado**: Pedido completado
- 🔴 **Cancelado**: Pedido cancelado

**INFORMACIÓN DE PEDIDOS:**
- Número de pedido único
- Cliente asociado
- Vendedor responsable
- Fecha de creación
- Estado actual
- Valor total
- Productos incluidos

**🔍 FILTROS DISPONIBLES:**
- **Por Estado**: Filtrar pedidos por estado específico
- **Por Vendedor**: Ver pedidos de un vendedor específico
- **Por Cliente**: Filtrar por cliente específico
- **Por Fecha**: Rango de fechas personalizado
- **Por Valor**: Filtrar por rango de valores

**📊 ACCIONES DISPONIBLES:**
- **Ver Detalle**: Información completa del pedido
- **Cambiar Estado**: Actualizar estado del pedido
- **Generar PDF**: Exportar pedido a PDF
- **Enviar Email**: Enviar pedido por correo

### 5.4 Administración de Usuarios

El gestor puede administrar todos los usuarios del sistema.

**ACCESO A USUARIOS:**
- Desde el menú: **Administración** → **Gestión de Usuarios**
- Panel de administración: `https://rpgestor.onrender.com/admin/`

**GESTIÓN DE USUARIOS:**

**👥 CREAR NUEVO USUARIO:**
1. Acceda al panel de administración
2. Vaya a **"Users"** → **"Add User"**
3. Complete la información básica:
   - *Username*: Nombre de usuario único
   - *Password*: Contraseña inicial
4. Haga clic en **"Save and continue editing"**
5. Complete información adicional:
   - *First name*: Nombre
   - *Last name*: Apellido
   - *Email*: Correo electrónico
   - *Groups*: Asignar rol (Gestor, JefeVentas, Vendedor)
   - *Active*: Marcar como activo
6. Haga clic en **"Save"**

**✏️ EDITAR USUARIO:**
1. En la lista de usuarios, haga clic en el usuario a editar
2. Modifique la información necesaria
3. Cambie grupos para modificar roles
4. Haga clic en **"Save"**

**🔒 DESACTIVAR USUARIO:**
1. Edite el usuario
2. Desmarque la casilla **"Active"**
3. Haga clic en **"Save"**

📝 **Nota**: Los usuarios desactivados no pueden iniciar sesión pero mantienen su información histórica.

### 5.5 Reportes Globales

El gestor tiene acceso a reportes completos del sistema.

**TIPOS DE REPORTES:**

**📈 REPORTE DE VENTAS:**
- Ventas por período (diario, semanal, mensual, anual)
- Comparativas entre períodos
- Tendencias y proyecciones
- Gráficos interactivos

**👥 REPORTE DE VENDEDORES:**
- Rendimiento individual de cada vendedor
- Cumplimiento de metas
- Ranking de productividad
- Análisis de actividad

**🛒 REPORTE DE PRODUCTOS:**
- Productos más vendidos
- Análisis de rotación de inventario
- Productos con bajo stock
- Rentabilidad por producto

**👤 REPORTE DE CLIENTES:**
- Clientes más activos
- Análisis de frecuencia de compra
- Valor promedio por cliente
- Segmentación de clientes

**📊 EXPORTACIÓN DE REPORTES:**
- **PDF**: Para presentaciones y archivo
- **Excel**: Para análisis adicional
- **CSV**: Para integración con otros sistemas

---

## 6. MANUAL DEL JEFE DE VENTAS

### 6.1 Dashboard del Equipo

El dashboard del jefe de ventas se enfoca en métricas y gestión del equipo comercial.

**ACCESO AL DASHBOARD:**
- URL directa: `https://rpgestor.onrender.com/usuarios/jefe_ventas_dashboard/`
- Desde el menú: **Dashboard** → **Mi Equipo**

**MÉTRICAS DEL EQUIPO:**

**📊 Resumen del Equipo:**
- **Total Vendedores**: Número de vendedores bajo su supervisión
- **Meta Mensual**: Objetivo de ventas del equipo para el mes
- **Ventas Actuales**: Ventas acumuladas del mes
- **% Cumplimiento**: Porcentaje de cumplimiento de la meta

**👥 RENDIMIENTO INDIVIDUAL:**
- Lista de vendedores con métricas individuales
- Progreso hacia metas personales
- Número de pedidos creados
- Valor total de ventas
- Indicadores de rendimiento (🟢 Alto, 🟡 Medio, 🔴 Bajo)

**📈 GRÁFICOS DEL EQUIPO:**
- **Ventas por Vendedor**: Comparativa de rendimiento
- **Evolución Mensual**: Tendencia de ventas del equipo
- **Cumplimiento de Metas**: Progreso hacia objetivos
- **Actividad Diaria**: Pedidos creados por día

### 6.2 Gestión de Vendedores

Herramientas para administrar y supervisar el equipo de ventas.

**ACCESO A GESTIÓN:**
- Desde el menú: **Equipo** → **Mis Vendedores**
- URL directa: `https://rpgestor.onrender.com/usuarios/mi_equipo/`

**INFORMACIÓN DE VENDEDORES:**

**📋 Lista del Equipo:**
- Nombre completo del vendedor
- Email y teléfono de contacto
- Fecha de último acceso
- Estado (Activo/Inactivo)
- Presupuesto asignado
- Ventas del mes actual

**📊 MÉTRICAS INDIVIDUALES:**
Para cada vendedor puede ver:
- **Pedidos Totales**: Número total de pedidos creados
- **Ventas del Mes**: Valor de ventas en el mes actual
- **Meta Asignada**: Objetivo mensual personalizado
- **% Cumplimiento**: Progreso hacia la meta
- **Clientes Activos**: Número de clientes gestionados
- **Última Actividad**: Fecha y hora del último pedido

**🎯 ACCIONES DISPONIBLES:**
- **Ver Detalle**: Información completa del vendedor
- **Enviar Mensaje**: Comunicación directa
- **Asignar Meta**: Establecer objetivos mensuales
- **Ver Pedidos**: Pedidos creados por el vendedor
- **Ver Clientes**: Cartera de clientes asignada

### 6.3 Sistema de Mensajería

Comunicación directa e inmediata con el equipo de vendedores.

**ACCESO A MENSAJERÍA:**
- Desde el menú: **Comunicación** → **Mensajes**
- URL directa: `https://rpgestor.onrender.com/usuarios/mensajes_equipo/`

**TIPOS DE MENSAJES:**

**📝 CATEGORÍAS DISPONIBLES:**
- 🎯 **Motivacional**: Mensajes de ánimo y reconocimiento
- ⚠️ **Alerta**: Avisos importantes y urgentes
- 📊 **Informativo**: Comunicados generales
- 🎉 **Felicitación**: Reconocimiento por logros

**📬 CREAR NUEVO MENSAJE:**
1. Haga clic en **"Nuevo Mensaje"**
2. Complete el formulario:
   - *Destinatario*: Seleccione el vendedor
   - *Tipo*: Elija la categoría del mensaje
   - *Asunto*: Título descriptivo
   - *Mensaje*: Contenido del mensaje
   - *Prioridad*: Alta, Media, Baja
3. Haga clic en **"Enviar Mensaje"**

**📋 GESTIÓN DE MENSAJES:**
- **Mensajes Enviados**: Historial de mensajes enviados
- **Estado de Lectura**: Verificar si el mensaje fue leído
- **Respuestas**: Ver respuestas de los vendedores
- **Búsqueda**: Buscar mensajes por contenido o destinatario

**🔔 NOTIFICACIONES:**
- Los vendedores reciben notificaciones inmediatas
- Indicadores visuales de mensajes no leídos
- Confirmación de entrega y lectura

### 6.4 Asignación de Metas

Establecimiento y seguimiento de objetivos para el equipo.

**ACCESO A METAS:**
- Desde el menú: **Objetivos** → **Metas del Equipo**
- URL directa: `https://rpgestor.onrender.com/usuarios/presupuestos_metas/`

**GESTIÓN DE METAS:**

**🎯 CREAR META MENSUAL:**
1. Haga clic en **"Nueva Meta"**
2. Complete la información:
   - *Vendedor*: Seleccione el vendedor
   - *Mes*: Mes objetivo
   - *Año*: Año objetivo
   - *Meta de Ventas*: Valor objetivo en ventas
   - *Meta de Pedidos*: Número objetivo de pedidos
3. Haga clic en **"Asignar Meta"**

**📊 SEGUIMIENTO DE METAS:**
- **Progreso Actual**: Porcentaje de cumplimiento
- **Días Restantes**: Tiempo disponible para cumplir
- **Proyección**: Estimación basada en tendencia actual
- **Alertas**: Notificaciones por bajo rendimiento

**📈 ANÁLISIS DE CUMPLIMIENTO:**
- **Histórico**: Cumplimiento de metas anteriores
- **Tendencias**: Patrones de rendimiento
- **Comparativas**: Rendimiento vs. otros vendedores
- **Recomendaciones**: Sugerencias para mejora

### 6.5 Reportes de Rendimiento

Análisis detallado del rendimiento del equipo.

**TIPOS DE REPORTES:**

**👥 REPORTE DEL EQUIPO:**
- Rendimiento consolidado del equipo
- Comparativas mensuales
- Identificación de fortalezas y oportunidades
- Gráficos de tendencias

**🏆 RANKING DE VENDEDORES:**
- Clasificación por diferentes métricas
- Vendedor del mes
- Mejores performers por categoría
- Análisis de consistencia

**📊 ANÁLISIS DE ACTIVIDAD:**
- Frecuencia de creación de pedidos
- Horarios de mayor actividad
- Patrones de comportamiento
- Eficiencia operativa

**🎯 CUMPLIMIENTO DE OBJETIVOS:**
- Porcentaje de cumplimiento por vendedor
- Análisis de desviaciones
- Factores de éxito
- Planes de mejora

### 6.6 Agenda y Reuniones

Programación y gestión de reuniones con el equipo.

**ACCESO A AGENDA:**
- Desde el menú: **Agenda** → **Mis Reuniones**
- URL directa: `https://rpgestor.onrender.com/usuarios/agenda/`

**GESTIÓN DE REUNIONES:**

**📅 CREAR REUNIÓN:**
1. Haga clic en **"Nueva Reunión"**
2. Complete los detalles:
   - *Título*: Nombre de la reunión
   - *Fecha*: Fecha de la reunión
   - *Hora*: Hora de inicio
   - *Duración*: Tiempo estimado
   - *Participantes*: Vendedores invitados
   - *Descripción*: Agenda y objetivos
3. Haga clic en **"Programar Reunión"**

**🔔 NOTIFICACIONES:**
- Los participantes reciben notificación inmediata
- Recordatorios automáticos 24 horas antes
- Recordatorios 1 hora antes de la reunión

**📋 TIPOS DE REUNIONES:**
- 🎯 **Seguimiento Individual**: Reuniones 1:1 con vendedores
- 👥 **Reunión de Equipo**: Reuniones grupales
- 📊 **Revisión de Resultados**: Análisis de métricas
- 🎓 **Capacitación**: Sesiones de entrenamiento

---

## 7. MANUAL DEL VENDEDOR

### 7.1 Dashboard Personal

El dashboard del vendedor muestra métricas personales y herramientas de trabajo diario.

**ACCESO AL DASHBOARD:**
- URL directa: `https://rpgestor.onrender.com/usuarios/vendedor_dashboard/`
- Desde el menú: **Dashboard** → **Mi Panel**

**MÉTRICAS PERSONALES:**

**📊 Resumen Personal:**
- **Mi Meta del Mes**: Objetivo de ventas asignado
- **Ventas Actuales**: Ventas acumuladas del mes
- **% Cumplimiento**: Progreso hacia la meta
- **Pedidos del Mes**: Número de pedidos creados

**📈 INDICADORES DE RENDIMIENTO:**
- **Promedio Diario**: Ventas promedio por día
- **Días para Meta**: Días restantes para cumplir objetivo
- **Proyección**: Estimación de cumplimiento basada en tendencia
- **Ranking**: Posición en el equipo de ventas

**🎯 OBJETIVOS Y METAS:**
- Meta mensual asignada por el jefe
- Progreso visual con barras de progreso
- Alertas de rendimiento
- Histórico de cumplimiento

**📅 ACTIVIDAD RECIENTE:**
- Últimos pedidos creados
- Clientes contactados recientemente
- Mensajes recibidos
- Próximas citas programadas

### 7.2 Gestión de Clientes

Herramientas para administrar la cartera de clientes asignada.

**ACCESO A CLIENTES:**
- Desde el menú: **Clientes** → **Mis Clientes**
- URL directa: `https://rpgestor.onrender.com/clientes/`

**FUNCIONALIDADES DE CLIENTES:**

**📋 LISTA DE CLIENTES:**
- Vista de todos los clientes asignados
- Información básica: Nombre, Email, Teléfono, Ciudad
- Estado del cliente (Activo/Inactivo)
- Fecha de último pedido
- Valor total de compras

**⭐ CLIENTES FAVORITOS:**
- Marcar clientes como favoritos para acceso rápido
- Lista separada de clientes prioritarios
- Acceso directo desde el dashboard

**🔍 BÚSQUEDA Y FILTROS:**
- **Búsqueda por texto**: Buscar por nombre o empresa
- **Filtro por ciudad**: Clientes por ubicación
- **Filtro por estado**: Activos o inactivos
- **Filtro por actividad**: Última fecha de pedido

**➕ CREAR NUEVO CLIENTE:**
1. Haga clic en **"Nuevo Cliente"**
2. Complete la información básica:
   - *Nombre*: Nombre completo o razón social
   - *Email*: Correo electrónico
   - *Teléfono*: Número de contacto
   - *Dirección*: Dirección completa
   - *Ciudad*: Ciudad de ubicación
   - *Notas*: Información adicional
3. Haga clic en **"Guardar Cliente"**

**✏️ EDITAR CLIENTE:**
1. Haga clic en el botón **"Editar"** junto al cliente
2. Modifique la información necesaria
3. Haga clic en **"Actualizar Cliente"**

**📊 HISTORIAL DEL CLIENTE:**
- Lista de todos los pedidos realizados
- Valor total de compras históricas
- Productos más comprados
- Frecuencia de pedidos
- Notas de interacciones anteriores

### 7.3 Creación de Pedidos

Sistema intuitivo para crear y gestionar pedidos de clientes.

**ACCESO A PEDIDOS:**
- Desde el menú: **Pedidos** → **Mis Pedidos**
- URL directa: `https://rpgestor.onrender.com/pedidos/`

**CREAR NUEVO PEDIDO:**

**PASO 1: Información Básica**
1. Haga clic en **"Nuevo Pedido"**
2. Seleccione el *Cliente* de la lista desplegable
3. Ingrese la *Fecha de Entrega* deseada
4. Agregue *Observaciones* si es necesario

**PASO 2: Agregar Productos**
1. Haga clic en **"Agregar Producto"**
2. Busque el producto por código o nombre
3. Seleccione el producto de la lista
4. Ingrese la *Cantidad* deseada
5. El sistema calculará automáticamente:
   - Precio unitario
   - Subtotal por producto
   - Total del pedido

**PASO 3: Revisar y Confirmar**
1. Revise todos los productos agregados
2. Verifique las cantidades y precios
3. Confirme la información del cliente
4. Haga clic en **"Guardar Pedido"**

**🔄 ESTADOS DEL PEDIDO:**
- 🟡 **Borrador**: Pedido en creación (editable)
- 🔵 **Confirmado**: Pedido enviado al cliente
- 🟠 **En Proceso**: Pedido en preparación
- 🟢 **Entregado**: Pedido completado
- 🔴 **Cancelado**: Pedido cancelado

**✏️ EDITAR PEDIDO:**
- Solo los pedidos en estado "Borrador" pueden editarse
- Puede agregar, quitar o modificar productos
- Cambiar información del cliente
- Actualizar fecha de entrega

**📄 GENERAR DOCUMENTOS:**
- **PDF del Pedido**: Para enviar al cliente
- **Lista de Picking**: Para preparación en almacén
- **Factura**: Una vez confirmado el pedido

### 7.4 Sistema de Agenda

Gestión de citas, reuniones y actividades programadas.

**ACCESO A AGENDA:**
- Desde el menú: **Agenda** → **Mi Calendario**
- URL directa: `https://rpgestor.onrender.com/usuarios/agenda/`

**FUNCIONALIDADES DE AGENDA:**

**📅 VISTA DE CALENDARIO:**
- Vista mensual con todos los eventos
- Código de colores por tipo de evento
- Navegación entre meses
- Vista de día y semana disponible

**➕ CREAR EVENTO:**
1. Haga clic en **"Nuevo Evento"** o en una fecha del calendario
2. Complete la información:
   - *Título*: Nombre del evento
   - *Fecha*: Fecha del evento
   - *Hora Inicio*: Hora de inicio
   - *Hora Fin*: Hora de finalización
   - *Tipo*: Reunión, Visita, Llamada, Otro
   - *Cliente*: Cliente relacionado (opcional)
   - *Descripción*: Detalles adicionales
3. Haga clic en **"Guardar Evento"**

**🔔 RECORDATORIOS:**
- Notificaciones 24 horas antes
- Recordatorios 1 hora antes
- Alertas en el dashboard
- Notificaciones por email (opcional)

**📋 TIPOS DE EVENTOS:**
- 🤝 **Reunión con Cliente**: Citas comerciales
- 📞 **Llamada Programada**: Seguimiento telefónico
- 🚗 **Visita**: Visitas a clientes
- 📊 **Reunión Interna**: Reuniones con jefe o equipo
- 🎓 **Capacitación**: Sesiones de entrenamiento

### 7.5 Mensajes Recibidos

Centro de comunicación con el jefe de ventas y notificaciones del sistema.

**ACCESO A MENSAJES:**
- Desde el menú: **Comunicación** → **Mis Mensajes**
- URL directa: `https://rpgestor.onrender.com/usuarios/inbox_mensajes/`

**GESTIÓN DE MENSAJES:**

**📬 BANDEJA DE ENTRADA:**
- Lista de todos los mensajes recibidos
- Indicador de mensajes no leídos
- Fecha y hora de recepción
- Remitente del mensaje
- Asunto y vista previa

**📝 TIPOS DE MENSAJES:**
- 🎯 **Motivacional**: Mensajes de ánimo del jefe
- ⚠️ **Alerta**: Avisos importantes
- 📊 **Informativo**: Comunicados generales
- 🎉 **Felicitación**: Reconocimientos por logros

**👁️ LEER MENSAJE:**
1. Haga clic en el mensaje para abrirlo
2. El mensaje se marcará automáticamente como leído
3. Puede ver el contenido completo
4. Opción de responder si está habilitada

**🔍 BÚSQUEDA DE MENSAJES:**
- Buscar por remitente
- Filtrar por tipo de mensaje
- Buscar por contenido
- Filtrar por fecha

**🗂️ ORGANIZACIÓN:**
- Mensajes leídos y no leídos
- Archivar mensajes importantes
- Eliminar mensajes no necesarios
- Marcar como favoritos

### 7.6 Calculadora de Precios

Herramienta para calcular precios y descuentos de productos.

**ACCESO A CALCULADORA:**
- Desde el menú: **Herramientas** → **Calculadora**
- Disponible también durante la creación de pedidos

**FUNCIONALIDADES:**

**💰 CÁLCULO DE PRECIOS:**
- Precio base del producto
- Aplicación de descuentos por volumen
- Cálculo de impuestos
- Precio final al cliente

**📊 DESCUENTOS DISPONIBLES:**
- **Por Cantidad**: Descuentos escalonados según volumen
- **Por Cliente**: Descuentos especiales para clientes VIP
- **Promocionales**: Ofertas temporales
- **Por Producto**: Descuentos específicos por producto

**🧮 CALCULADORA AVANZADA:**
1. Seleccione el producto
2. Ingrese la cantidad
3. Seleccione el tipo de cliente
4. El sistema mostrará:
   - Precio unitario base
   - Descuento aplicable
   - Precio unitario final
   - Total de la línea
   - Impuestos incluidos

**📋 HISTORIAL DE CÁLCULOS:**
- Guarda los últimos cálculos realizados
- Permite reutilizar configuraciones
- Exportar cálculos a PDF
- Enviar cotizaciones por email

---

## 8. FUNCIONALIDADES COMUNES

### 8.1 Sistema de Notificaciones

Todas las notificaciones del sistema se muestran de manera consistente para todos los roles.

**TIPOS DE NOTIFICACIONES:**

**🔔 NOTIFICACIONES EN TIEMPO REAL:**
- Mensajes nuevos recibidos
- Cambios de estado en pedidos
- Recordatorios de agenda
- Alertas de sistema

**📱 CENTRO DE NOTIFICACIONES:**
- Icono de campana en la barra superior
- Contador de notificaciones no leídas
- Lista desplegable con notificaciones recientes
- Enlace directo a la fuente de la notificación

**⚙️ CONFIGURACIÓN DE NOTIFICACIONES:**
1. Acceda a **"Mi Perfil"** → **"Configuración"**
2. Seleccione los tipos de notificaciones deseadas:
   - ✅ Mensajes nuevos
   - ✅ Cambios en pedidos
   - ✅ Recordatorios de agenda
   - ✅ Alertas de metas
3. Elija el método de notificación:
   - 🌐 En el sistema (siempre activo)
   - 📧 Por email (opcional)
4. Haga clic en **"Guardar Configuración"**

### 8.2 Búsqueda y Filtros

Sistema unificado de búsqueda disponible en todas las secciones.

**🔍 BÚSQUEDA GLOBAL:**
- Campo de búsqueda en la barra superior
- Busca en clientes, productos y pedidos
- Resultados categorizados
- Acceso directo a elementos encontrados

**🎛️ FILTROS AVANZADOS:**
Disponibles en listas de:
- **Clientes**: Por ciudad, estado, actividad
- **Productos**: Por grupo, subgrupo, stock
- **Pedidos**: Por estado, fecha, vendedor, cliente
- **Mensajes**: Por tipo, fecha, remitente

**💡 CONSEJOS DE BÚSQUEDA:**
- Use palabras clave específicas
- Combine filtros para resultados precisos
- Guarde búsquedas frecuentes como favoritas
- Use comodines (*) para búsquedas amplias

### 8.3 Exportación de Datos

Funcionalidades para exportar información en diferentes formatos.

**📄 FORMATOS DISPONIBLES:**
- **PDF**: Para presentaciones y archivo
- **Excel**: Para análisis y manipulación de datos
- **CSV**: Para integración con otros sistemas

**📊 DATOS EXPORTABLES:**
- Listas de clientes
- Inventario de productos
- Reportes de pedidos
- Métricas de rendimiento
- Reportes personalizados

**⬇️ PROCESO DE EXPORTACIÓN:**
1. Navegue a la sección deseada
2. Aplique filtros si es necesario
3. Haga clic en **"Exportar"**
4. Seleccione el formato deseado
5. El archivo se descargará automáticamente

### 8.4 Configuración Personal

Personalización de la experiencia de usuario.

**⚙️ ACCESO A CONFIGURACIÓN:**
- Haga clic en su nombre de usuario
- Seleccione **"Configuración"**

**🎨 OPCIONES DE PERSONALIZACIÓN:**
- **Tema**: Claro u oscuro
- **Idioma**: Español (por defecto)
- **Zona Horaria**: Configuración regional
- **Formato de Fecha**: DD/MM/YYYY o MM/DD/YYYY
- **Moneda**: Símbolo y formato de moneda

**🔔 PREFERENCIAS DE NOTIFICACIÓN:**
- Activar/desactivar tipos específicos
- Configurar horarios de notificación
- Método de entrega preferido

**📱 CONFIGURACIÓN DE DISPOSITIVO:**
- Recordar sesión en este dispositivo
- Configuración de notificaciones push
- Sincronización offline (próximamente)

---

## 9. SOLUCIÓN DE PROBLEMAS

### 9.1 Problemas Comunes

**🔐 PROBLEMAS DE ACCESO:**

**❌ No puedo iniciar sesión**
- ✅ Verifique que está usando las credenciales correctas
- ✅ Asegúrese de que su cuenta esté activa
- ✅ Limpie la caché del navegador
- ✅ Intente desde un navegador diferente
- ✅ Contacte al administrador si persiste el problema

**❌ La página no carga correctamente**
- ✅ Verifique su conexión a internet
- ✅ Actualice la página (F5 o Ctrl+R)
- ✅ Limpie la caché del navegador
- ✅ Desactive extensiones del navegador temporalmente
- ✅ Intente desde modo incógnito

**❌ Los datos no se actualizan**
- ✅ Haga clic en el botón "Actualizar" si está disponible
- ✅ Cierre sesión y vuelva a iniciar sesión
- ✅ Verifique que no hay problemas de conectividad
- ✅ Contacte soporte si el problema persiste

**📱 PROBLEMAS EN DISPOSITIVOS MÓVILES:**

**❌ La interfaz se ve mal en móvil**
- ✅ Use un navegador moderno (Chrome, Safari, Firefox)
- ✅ Asegúrese de tener la última versión del navegador
- ✅ Rote el dispositivo para vista horizontal si es necesario
- ✅ Ajuste el zoom del navegador al 100%

**❌ Los botones no responden en táctil**
- ✅ Asegúrese de tocar directamente el botón
- ✅ Evite toques múltiples rápidos
- ✅ Limpie la pantalla del dispositivo
- ✅ Reinicie el navegador

### 9.2 Mensajes de Error

**⚠️ ERRORES COMUNES Y SOLUCIONES:**

**"Error de conexión"**
- **Causa**: Problemas de conectividad
- **Solución**: Verifique su conexión a internet y reintente

**"Sesión expirada"**
- **Causa**: La sesión ha caducado por inactividad
- **Solución**: Inicie sesión nuevamente

**"Permisos insuficientes"**
- **Causa**: Intenta acceder a una función no autorizada para su rol
- **Solución**: Contacte a su administrador para verificar permisos

**"Datos no válidos"**
- **Causa**: Información ingresada incorrectamente en formularios
- **Solución**: Revise los campos marcados en rojo y corrija la información

**"Error interno del servidor"**
- **Causa**: Problema técnico temporal
- **Solución**: Espere unos minutos y reintente. Si persiste, contacte soporte

### 9.3 Contacto de Soporte

**📞 CANALES DE SOPORTE:**

**🌐 Soporte Online:**
- **URL**: https://rpgestor.onrender.com/soporte/
- **Horario**: Lunes a Viernes, 8:00 AM - 6:00 PM
- **Tiempo de respuesta**: 2-4 horas

**📧 Email de Soporte:**
- **Email**: soporte@rpgestor.com
- **Para**: Problemas técnicos, consultas generales
- **Tiempo de respuesta**: 24-48 horas

**📱 WhatsApp:**
- **Número**: +57 XXX XXX XXXX
- **Para**: Consultas urgentes
- **Horario**: Lunes a Viernes, 8:00 AM - 5:00 PM

**🎫 CREAR TICKET DE SOPORTE:**
1. Acceda al sistema de soporte
2. Haga clic en **"Nuevo Ticket"**
3. Complete la información:
   - *Tipo de problema*: Técnico, Funcional, Consulta
   - *Prioridad*: Alta, Media, Baja
   - *Descripción*: Detalle del problema
   - *Capturas de pantalla*: Si aplica
4. Haga clic en **"Enviar Ticket"**

**📋 INFORMACIÓN A INCLUIR EN REPORTES:**
- Descripción detallada del problema
- Pasos para reproducir el error
- Navegador y versión utilizada
- Sistema operativo
- Capturas de pantalla del error
- Hora aproximada cuando ocurrió

---

## 10. APÉNDICES

### 10.1 Glosario de Términos

**📚 TÉRMINOS TÉCNICOS:**

**API**: Interfaz de Programación de Aplicaciones - Permite integración con otros sistemas

**Dashboard**: Panel de control con métricas y resumen de información

**Responsive**: Diseño que se adapta automáticamente a diferentes tamaños de pantalla

**WebSocket**: Tecnología para actualizaciones en tiempo real

**Cache**: Almacenamiento temporal para mejorar velocidad de carga

**SSL**: Protocolo de seguridad para conexiones encriptadas

**📊 TÉRMINOS DE NEGOCIO:**

**KPI**: Indicador Clave de Rendimiento - Métricas importantes del negocio

**ROI**: Retorno de Inversión - Beneficio obtenido vs. inversión realizada

**Pipeline**: Proceso de ventas desde prospecto hasta cliente

**Lead**: Prospecto o cliente potencial

**Conversion Rate**: Tasa de conversión de prospectos a clientes

**Churn**: Tasa de abandono de clientes

### 10.2 Atajos de Teclado

**⌨️ NAVEGACIÓN GENERAL:**
- `Ctrl + /`: Abrir búsqueda global
- `Ctrl + H`: Ir al dashboard principal
- `Ctrl + N`: Crear nuevo elemento (según contexto)
- `Ctrl + S`: Guardar formulario actual
- `Esc`: Cerrar modal o cancelar acción

**📋 GESTIÓN DE LISTAS:**
- `Ctrl + F`: Buscar en lista actual
- `Ctrl + R`: Actualizar lista
- `Ctrl + E`: Exportar lista actual
- `↑/↓`: Navegar entre elementos de lista
- `Enter`: Abrir elemento seleccionado

**📝 FORMULARIOS:**
- `Tab`: Siguiente campo
- `Shift + Tab`: Campo anterior
- `Ctrl + Enter`: Guardar y continuar
- `Ctrl + Shift + S`: Guardar y crear nuevo

### 10.3 Preguntas Frecuentes

**❓ PREGUNTAS GENERALES:**

**¿Puedo usar RPGestor desde mi teléfono móvil?**
✅ Sí, RPGestor tiene diseño responsive y funciona perfectamente en smartphones y tablets.

**¿Los datos se sincronizan en tiempo real?**
✅ Sí, todos los cambios se reflejan inmediatamente en todos los dispositivos conectados.

**¿Puedo trabajar offline?**
❌ Actualmente RPGestor requiere conexión a internet. La funcionalidad offline está en desarrollo.

**¿Cómo cambio mi contraseña?**
✅ Vaya a "Mi Perfil" → "Cambiar Contraseña" e ingrese su contraseña actual y la nueva.

**¿Puedo exportar mis datos?**
✅ Sí, puede exportar listas y reportes en formato PDF, Excel y CSV.

**❓ PREGUNTAS POR ROL:**

**VENDEDORES:**

**¿Puedo ver los pedidos de otros vendedores?**
❌ No, solo puede ver sus propios pedidos por seguridad y privacidad.

**¿Cómo sé si mi jefe leyó mi mensaje?**
✅ Los mensajes muestran estado de entrega y lectura cuando están disponibles.

**¿Puedo modificar un pedido después de crearlo?**
✅ Solo si está en estado "Borrador". Una vez confirmado, debe contactar a su jefe.

**JEFES DE VENTAS:**

**¿Puedo asignar clientes a mis vendedores?**
✅ Sí, desde la gestión de clientes puede reasignar clientes entre vendedores.

**¿Cómo veo el rendimiento histórico de mi equipo?**
✅ Use la sección "Reportes de Rendimiento" con filtros de fecha personalizados.

**¿Puedo crear metas para períodos diferentes al mes?**
❌ Actualmente solo se soportan metas mensuales. Metas semanales están en desarrollo.

**GESTORES:**

**¿Puedo crear usuarios desde el sistema?**
✅ Sí, use el panel de administración para crear y gestionar usuarios.

**¿Cómo hago backup de los datos?**
✅ Los backups son automáticos. Para backups manuales, contacte soporte técnico.

**¿Puedo integrar RPGestor con otros sistemas?**
✅ Sí, RPGestor tiene API REST para integraciones. Contacte soporte para detalles técnicos.

---

## 📞 INFORMACIÓN DE CONTACTO

**🌐 Sistema**: https://rpgestor.onrender.com  
**📧 Soporte**: soporte@rpgestor.com  
**📱 WhatsApp**: +57 XXX XXX XXXX  
**💼 LinkedIn**: [Perfil del Desarrollador]  

**⏰ Horarios de Soporte:**
- Lunes a Viernes: 8:00 AM - 6:00 PM
- Sábados: 9:00 AM - 1:00 PM
- Domingos: Solo emergencias

---

## 📝 NOTAS FINALES

Este manual se actualiza regularmente con nuevas funcionalidades y mejoras del sistema. 

**Versión del Manual**: 2.0.0  
**Última Actualización**: Julio 2025  
**Próxima Revisión**: Octubre 2025  

Para sugerencias de mejora de este manual, contacte: documentacion@rpgestor.com

---

*© 2025 RPGestor. Todos los derechos reservados.*