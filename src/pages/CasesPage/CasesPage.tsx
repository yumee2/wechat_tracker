import React from 'react';
import CardComponent from './CardComponents/CardComponent';
import styles from './style.module.css';

const CasesPage: React.FC = () => {
  const products = [
    { id: '1', image: '/lojka1.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '2', image: '/lojka2.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '3', image: '/lojka3.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '4', image: '/images/product4.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '5', image: '/images/product1.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '6', image: '/images/product2.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '7', image: '/images/product3.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
    { id: '8', image: '/images/product4.jpg', newPrice: 300, oldPrice: 800, title: 'Обувные ложки', deliveryTime: 30 },
  ];

  return (
    <div className={styles.casesPage}>
      <div className={styles.cardsContainer}>
        {products.map((product, index) => (
          <CardComponent
            key={index}
            id={product.id}
            image={product.image}
            newPrice={product.newPrice}
            oldPrice={product.oldPrice}
            title={product.title}
            deliveryTime={product.deliveryTime}
          />
        ))}
      </div>
    </div>
  );
};

export default CasesPage;
