# Arquitetura

O projeto foi organizado para separar o dominio do mural das configuracoes gerais do Django.

## Apps

`apps.dashboard` concentra as regras do mural:

- `models.py`: entidades editaveis no admin, mapeadas para tabelas existentes do banco.
- `admin.py`: telas de manutencao para equipe administrativa.
- `views.py`: montagem do painel publico.
- `services/weather.py`: cliente da API de clima.

`apps.core` guarda recursos compartilhados. No momento, inclui o comando `seed_demo`.

## Modelos principais

- `Turma`: dados de curso, ano escolar, turno e situacao.
- `Permissao`: niveis de permissao dos usuarios.
- `Usuario`: contas do sistema, vinculo com turma, permissao e dados de acesso.
- `Disciplina`: componentes curriculares e status.
- `Aviso`: comunicados com periodo de publicacao e status.
- `Evento`: agenda institucional com data/horario e status.
- `Professor`: docentes vinculados aos horarios.
- `Horario`: aulas por turma, disciplina, professor, dia da semana, periodo e intervalo de horario.

## Clima

A integracao usa Open-Meteo para evitar chave obrigatoria em desenvolvimento. As coordenadas ficam nas variaveis `WEATHER_LATITUDE` e `WEATHER_LONGITUDE`.

O endpoint publico `/api/clima/` devolve o mesmo objeto usado pelo painel, em JSON.

Em producao, recomenda-se adicionar cache no servico de clima para atualizar em intervalos previsiveis, por exemplo a cada 10 ou 15 minutos.
