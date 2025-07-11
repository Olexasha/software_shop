#!/bin/bash -e

echo "⚙️  Загрузка фикстур началась..."

# Ожидание готовности БД (можно опустить, если зависит от service_completed_successfully)
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "⏳ Ожидаем доступности PostgreSQL..."
  sleep 2
done

# Путь до manage.py
PROJECT_DIR="/software_shop/software_shop"
FIXTURES_DIR="${PROJECT_DIR}/fixtures"
MANAGE="${PROJECT_DIR}/manage.py"

if [[ ! -f "$MANAGE" ]]; then
  echo "❌ Не найден manage.py: $MANAGE"
  exit 1
fi

# Упорядоченные файлы
order_files=(
  "users_customuser.json"
  "subscriptions_tariff.json"
  "subscriptions_usersubscription.json"
  "products_product.json"
  "products_productvariant.json"
  "products_purchase.json"
)

# Загружаем в порядке
for filename in "${order_files[@]}"; do
  path="${FIXTURES_DIR}/${filename}"
  if [[ -f "$path" ]]; then
    echo "📥 Загружаем: $filename"
    python "$MANAGE" loaddata "$path"
  else
    echo "⚠️  Пропущен (не найден): $filename"
  fi
done

# Загружаем оставшиеся
find "$FIXTURES_DIR" -type f -name "*.json" | while read -r file; do
  skip=false
  for ordered in "${order_files[@]}"; do
    if [[ "$file" == *"$ordered" ]]; then
      skip=true
      break
    fi
  done
  if [[ "$skip" == false ]]; then
    echo "📥 Загружаем (неупорядоченный): $(basename "$file")"
    python "$MANAGE" loaddata "$file"
  fi
done

echo "✅ Загрузка фикстур завершена!"
