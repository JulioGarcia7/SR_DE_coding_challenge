# Tareas Pendientes

## Limpieza y Organización
- [ ] Eliminar directorio `app/api/models/gold/`
- [ ] Actualizar referencias a la capa gold en la documentación

## Implementación de API
- [ ] Crear rutas para la capa Bronze (staging):
  - [ ] POST `/api/v1/bronze/upload/departments`
  - [ ] POST `/api/v1/bronze/upload/jobs`
  - [ ] POST `/api/v1/bronze/upload/hired_employees`

- [ ] Crear rutas para la capa Silver:
  - [ ] GET `/api/v1/silver/departments`
  - [ ] GET `/api/v1/silver/jobs`
  - [ ] GET `/api/v1/silver/hired_employees`

## Testing
- [ ] Implementar tests para modelos
- [ ] Implementar tests para schemas
- [ ] Implementar tests para rutas Bronze
- [ ] Implementar tests para rutas Silver

## Migraciones
- [ ] Crear migración inicial para tablas staging
- [ ] Crear migración para tablas dimensionales

## Documentación
- [ ] Agregar documentación de API
- [ ] Agregar guía de pruebas
- [ ] Agregar documentación de proceso ETL

## Proceso ETL
- [ ] Implementar proceso de truncate-insert para staging
- [ ] Implementar transformaciones de staging a dimensional
- [ ] Agregar validaciones de datos
- [ ] Implementar manejo de errores 