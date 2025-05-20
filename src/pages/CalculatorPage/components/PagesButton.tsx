import React from 'react';
import styles from './styles.module.css'

interface ButtonProps {
  src: string;
  alt: string;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({ src, alt, onClick }) => {
  return (
    <button onClick={onClick} className={styles.uiButton}>
      <img src={src} alt={alt} className={styles.buttonImage} />
    </button>
  );
}

export default Button;
