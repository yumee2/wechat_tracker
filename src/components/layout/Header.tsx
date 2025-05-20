import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../../pages/CalculatorPage/components/PagesButton';
import styles from './styles.module.css'

const Header: React.FC = () => {
  const handleClick = (buttonName: string) => {
    alert(`${buttonName} нажата!`);
  };

  return (
    <header className={styles.header}>
      <div className={styles.buttonGroup}>
        <Link to="/"><Button src="/trackingButton.png" alt="Кнопка 1" /></Link>
        <Link to="/currency"><Button src="/calculatorButton.png" alt="Кнопка 2" /></Link>
        <Link to="/currency"><Button src="/currencyButton.png" alt="Кнопка 3" /></Link>
        <Link to="/cases"><Button src="/casesButton.png" alt="Кнопка 4" /></Link>
      </div>
    </header>
  );
};

export default Header;
