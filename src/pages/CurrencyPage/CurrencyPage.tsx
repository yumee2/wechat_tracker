import React from 'react';
import CurrencyBlock from './components/CurrencyBlock';
import styles from './style.module.css';

const CurrencyPage: React.FC = () => {
  const currencyData = [
    {
      currencyCode: 'CNY',
      cardRate1: 11.41,  // Основной курс для карты
      cardRate2: 0.14,   // Дополнительный курс для карты
      cashRate1: 11.41,  // Основной курс для наличных
      cashRate2: 0.14,   // Дополнительный курс для наличных
      IconUp: `
        <svg width="20" height="17" viewBox="0 0 20 17" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10 17L0.473721 0.5L19.5263 0.5L10 17Z" fill="#00FF09"/>
        </svg>
      `,
      IconDown: `
        <svg width="20" height="17" viewBox="0 0 20 17" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M10 0.5L19.5263 17H0.473721L10 0.5Z" fill="#FF0000"/>
        </svg>
      `,
    }
  ];

  return (
    <div className={styles.currencyPage}>
      <div className={styles.currencyBlock}>
        {currencyData.map((currency, index) => (
          <CurrencyBlock
            key={index}
            currencyCode={currency.currencyCode}
            cardRate1={currency.cardRate1}
            cardRate2={currency.cardRate2}
            cashRate1={currency.cashRate1}
            cashRate2={currency.cashRate2}
            IconUp={currency.IconUp}
            IconDown={currency.IconDown}
          />
        ))}
      </div>
    </div>
  );
};

export default CurrencyPage;