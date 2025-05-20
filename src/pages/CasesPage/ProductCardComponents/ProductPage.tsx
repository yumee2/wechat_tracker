import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import styles from './styles.module.css';
import FullscreenImageModal from '../FullScreenImage/FullScreenImage';

// Импортируем SVG стрелочки для кнопки "назад"
const BackArrow = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M15 18L9 12L15 6" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ProductPage: React.FC = () => {
  const navigate = useNavigate();
  const { productId } = useParams<{ productId: string }>();
  
  // В реальном приложении здесь будет запрос к API для получения данных о товаре
  // Пока используем mock данные
  const product = {
    id: productId,
    title: 'Обувные ложки',
    images: [
      '/lojka1.jpg',
      '/lojka2.jpg',
      '/lojka3.jpg',
    ],
    newPrice: 300,
    oldPrice: 800,
    deliveryTime: 30,
    description: 'Lorem ipsum dolor sit amet consectetur. Facilisis egestas pellentesque auctor velit justo facilisis purus. Pellentesque odio velit quis turpis. Arcu faucibus consectetur duis diam. Vel aliquam convallis lacinia cras.'
  };

  const [currentImageIndex, setCurrentImageIndex] = React.useState(0);
  const [transitionDirection, setTransitionDirection] = 
  React.useState<'forward' | 'backward'>('forward');
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const closeModal = () => setIsModalOpen(false);

  const nextImage = () => {
    setTransitionDirection('forward');
    setCurrentImageIndex((prev) => 
      prev === product.images.length - 1 ? 0 : prev + 1
    );
  };

  const prevImage = () => {
    setTransitionDirection('backward');
    setCurrentImageIndex((prev) => 
      prev === 0 ? product.images.length - 1 : prev - 1
    );
  };

  return (
    <div className={styles.productPage}>
      <div className={styles.header}>
        <button className={styles.backButton} onClick={() => navigate(-1) || navigate('/cases')}>
          <BackArrow />
        </button>
        <h1 className={styles.title}>{product.title}</h1>
      </div>

      <div className={styles.imageContainer} onClick={() => setIsModalOpen(true)}>
        <img 
          key={currentImageIndex}
          src={product.images[currentImageIndex]} 
          alt={product.title} 
          className={`${styles.productImage} ${styles[transitionDirection]}`}
        />
        {product.images.length > 1 && (
          <>
            <button 
              className={`${styles.navButton} ${styles.prevButton}`} 
              onClick={(e) => {
                e.stopPropagation();
                prevImage();
              }}
            >
              ‹
            </button>
            <button 
              className={`${styles.navButton} ${styles.nextButton}`} 
              onClick={(e) => {
                e.stopPropagation();
                nextImage();
              }}
            >
              ›
            </button>
          </>
        )}
      </div>

      <div className={styles.priceDeliveryRow}>
        <div className={styles.priceContainer}>
          <span className={styles.newPrice}>{product.newPrice} ₽</span>
          <span className={styles.oldPrice}>{product.oldPrice} ₽</span>
        </div>
        <div className={styles.deliveryInfo}>
          Доставка: {product.deliveryTime} дней
        </div>
      </div>

      <div className={styles.description}>
        {product.description}
      </div>

      <button className={styles.contactButton}>
        НАПИСАТЬ
      </button>
      {isModalOpen && (
        <FullscreenImageModal
          images={product.images}
          currentIndex={currentImageIndex}
          onClose={closeModal}
          title={product.title}
        />
      )}
    </div>
  );
};

export default ProductPage;