
import React, { useState } from 'react';
import styles from './style.module.css';
import { isInRange, isValidNumber, isValidBoxCount } from '../../utils/ValidateCalculator';

interface CalculatorState {
  productType: string;
  kg: string;
  width: string;
  height: string;
  length: string;
  boxCount: string;
  unit: string;
}

const CalculatorPage: React.FC = () => {
  const [formData, setFormData] = useState<CalculatorState>({
    productType: '',
    kg: '',
    width: '',
    height: '',
    length: '',
    boxCount: '',
    unit: 'см',
  });

  const [errors, setErrors] = useState<Partial<CalculatorState>>({});

  const productTypes = ['Товар 1', 'Товар 2', 'Товар 3'];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleProductTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData((prevData) => ({
      ...prevData,
      productType: e.target.value,
    }));
  };

  const handleUnitChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData((prevData) => ({
      ...prevData,
      unit: e.target.value,
    }));
  };

  // Логика валидации формы
  const validateForm = () => {
    let isValid = true;
    let newErrors: Partial<CalculatorState> = {};

    // Валидация поля "productType" (должен быть выбран товар)
    if (!formData.productType) {
      newErrors.productType = 'Выберите товар';
      isValid = false;
    }

    // Валидация поля "kg" (должно быть положительным числом)
    if (!isValidNumber(formData.kg)) {
      newErrors.kg = 'Введите корректное значение для кг';
      isValid = false;
    }

    // Валидация поля "width" (должно быть числом в пределах от 0 до 1000)
    if (!isInRange(formData.width, 0, 1000)) {
      newErrors.width = 'Ширина должна быть в пределах от 0 до 1000';
      isValid = false;
    }

    // Валидация поля "height"
    if (!isInRange(formData.height, 0, 1000)) {
      newErrors.height = 'Высота должна быть в пределах от 0 до 1000';
      isValid = false;
    }

    // Валидация поля "length"
    if (!isInRange(formData.length, 0, 1000)) {
      newErrors.length = 'Длина должна быть в пределах от 0 до 1000';
      isValid = false;
    }

    // Валидация поля "boxCount" (целое положительное число)
    if (!isValidBoxCount(formData.boxCount)) {
      newErrors.boxCount = 'Количество коробок должно быть целым числом';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleCalculate = () => {
    if (validateForm()) {
      alert('Калькуляция завершена!');
    }
  };
  return (
    <div className={styles.calculatorPage}>
        <div className={styles.titleContainer}>
            <div className={styles.svgContainer}>
                <svg width="37" height="37" viewBox="0 0 37 37" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7.61913 29.3807C9.57174 31.3333 12.7144 31.3333 18.9998 31.3333C25.2852 31.3333 28.428 31.3333 30.3805 29.3807C32.3332 27.4281 32.3332 24.2853 32.3332 18C32.3332 11.7146 32.3332 8.5719 30.3805 6.61929C28.428 4.66666 25.2852 4.66666 18.9998 4.66666C12.7144 4.66666 9.57174 4.66666 7.61913 6.61929C5.6665 8.5719 5.6665 11.7146 5.6665 18C5.6665 24.2853 5.6665 27.4281 7.61913 29.3807Z" stroke="#1C274D" stroke-width="1.5"/>
                <path opacity="0.5" d="M27 13.3333H21.6667M27 21.3333H21.6667M27 25.3333H21.6667M16.3333 13.3333H13.6667M13.6667 13.3333H11M13.6667 13.3333V10.6666M13.6667 13.3333V16M15.6667 21.3333L13.6667 23.3333M13.6667 23.3333L11.6667 25.3333M13.6667 23.3333L11.6667 21.3333M13.6667 23.3333L15.6667 25.3333" stroke="#1C274D" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
            </div>
            <h2 className={styles.title}>Калькулятор доставки</h2>
        </div>
      
      <div className={styles.formContainer}>
        <div className={styles.inputRow}>
          <select
            name="productType"
            value={formData.productType}
            onChange={handleProductTypeChange}
            className={`${styles.select} ${errors.productType ? styles.inputError : ''}`}
          >
            <option value="">Выберите тип товара</option>
            {productTypes.map((type, index) => (
              <option key={index} value={type}>
                {type}
              </option>
            ))}
          </select>
          <input
            type="number"
            name="kg"
            value={formData.kg}
            min={0}
            onChange={handleInputChange}
            placeholder="кг"
            className={`${styles.input} ${errors.kg ? styles.inputError : ''}`}
          />
        </div>

        <div className={styles.inputRow}>
          <input
            type="number"
            name="width"
            min={0}
            value={formData.width}
            onChange={handleInputChange}
            placeholder="Ширина"
            className={`${styles.input} ${errors.width ? styles.inputError : ''}`}
          />
          {/* {errors.width && <div className={styles.error}>{errors.width}</div>} */}
        </div>

        <div className={styles.inputRow}>
          <input
            type="number"
            name="height"
            min={0}
            value={formData.height}
            onChange={handleInputChange}
            placeholder="Высота"
            className={`${styles.input} ${errors.height ? styles.inputError : ''}`}
          />
          {/* {errors.height && <div className={styles.error}>{errors.height}</div>} */}
        </div>

        <div className={styles.inputRow}>
          <input
            type="number"
            name="length"
            min={0}
            value={formData.length}
            onChange={handleInputChange}
            placeholder="Длина"
           className={`${styles.input} ${errors.length ? styles.inputError : ''}`}
          />
          {/* {errors.length && <div className={styles.error}>{errors.length}</div>} */}
        </div>

        <div className={styles.inputRow}>
          <input
            type="number"
            name="boxCount"
            min={0}
            value={formData.boxCount}
            onChange={handleInputChange}
            placeholder="Количество коробок"
           className={`${styles.input} ${errors.boxCount ? styles.inputError : ''}`}
          />
          {/* {errors.boxCount && <div className={styles.error}>{errors.boxCount}</div>} */}
        </div>

        <div className={styles.inputRow}>
          <select
            name="unit"
            value={formData.unit}
            onChange={handleUnitChange}
            className={`${styles.select} ${styles.selectUnit}`}
          >
            <option value="см">см</option>
            <option value="м">м</option>
            <option value="дюйм">дюйм</option>
          </select>
          <button className={styles.calculateButton} onClick={handleCalculate}>
            РАССЧИТАТЬ
          </button>
        </div>
      </div>
      <div className={styles.boxImage}>
        <img src="/box.png" alt="Коробка" />
      </div>
    </div>
  );
};

export default CalculatorPage;
