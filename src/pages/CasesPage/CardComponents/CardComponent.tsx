import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './styles.module.css';

interface CardComponentProps {
  id: string,
  image: string;
  title: string;
  newPrice: number;
  oldPrice: number;
  deliveryTime: number;
}

const CardComponent: React.FC<CardComponentProps> = ({ id, image, title, newPrice, oldPrice, deliveryTime }) => {
  const navigate = useNavigate();
  return (
    <div 
      className={styles.card}
      onClick={() => navigate(`/product/${id}`)}
      style={{ cursor: 'pointer' }}
    >
      <img src={image} alt={title} className={styles.cardImage} />
      <div className={styles.cardContent}>
        <div className={styles.priceContainer}>
          <div className={styles.newPrice}>
            {newPrice} <span className={styles.currency}>₽</span>
          </div>
          <div className={styles.oldPrice}>
            {oldPrice} <span className={styles.currency}>₽</span>
          </div>
        </div>
        
        <h3 className={styles.cardTitle}>{title}</h3>
        <div className={styles.cardDeliveryTime}>
          Доставка: {deliveryTime} дней
        </div>
      </div>
    </div>
  );
};

export default CardComponent;