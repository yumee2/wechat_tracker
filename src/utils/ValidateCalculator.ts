
// Проверка на целое положительное число
export const isPositiveInteger = (value: string): boolean => {
  const number = parseInt(value, 10);
  return !isNaN(number) && number >= 0 && Number.isInteger(number);
};

// Проверка на допустимый диапазон
export const isInRange = (value: string, min: number, max: number): boolean => {
  const number = parseFloat(value);
  return !isNaN(number) && number >= min && number <= max;
};

// Проверка на корректность ввода числа
export const isValidNumber = (value: string) => {
  const numberValue = Number(value);
  return !isNaN(numberValue) && numberValue > 0;
};

// Дополнительная валидация на типы данных
export const isValidBoxCount = (value: string): boolean => {
  return isPositiveInteger(value);
};
