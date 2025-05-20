import React from 'react';
import styles from './style.module.css';

interface CurrencyBlockProps {
  currencyCode: string;
  cardRate1: number;  // Первый курс при оплате картой
  cardRate2: number;  // Второй курс при оплате картой
  cashRate1: number;  // Первый курс при оплате наличными
  cashRate2: number;  // Второй курс при оплате наличными
  IconUp: string;   // Иконка для карты
  IconDown: string;   // Иконка для наличных
}

const CurrencyBlock: React.FC<CurrencyBlockProps> = ({
  currencyCode,
  cardRate1,
  cardRate2,
  cashRate1,
  cashRate2,
  IconUp,
  IconDown
}) => {
  return (
    <div className={styles.currencyPage}>
        <div className={styles.currencyBlock}>
            <div className={styles.cardBlock}>
                <div className={styles.cardTitle}>Картой</div>
                <div className={styles.cardPriceBlock}>
                    <div className={styles.cardPriceLeft}>
                        <div className={styles.leftUpPart}>
                            <div className={styles.CurrencyTitle}>{currencyCode}</div>
                            <div className={styles.CurrencyIcon} dangerouslySetInnerHTML={{ __html: IconUp }}>
                            </div>
                        </div>
                        <div className={styles.price}>{cardRate1}<span>₽</span></div>
                    </div>

                    <div className={styles.cardPriceRight}>
                        <div className={styles.rightUpPart}>
                            <div className={styles.CurrencyTitle}>{currencyCode}</div>
                            <div className={styles.CurrencyIcon} dangerouslySetInnerHTML={{ __html: IconDown }}>
                                
                            </div>
                        </div>
                        <div className={styles.price}>{cardRate2}<span>₽</span></div>
                    </div>
                </div>
            </div>
            <div className={styles.cashBlock}>
                <div className={styles.cardTitle}>Наличка</div>
                <div className={styles.cardPriceBlock}>
                    <div className={styles.cardPriceLeft}>
                        <div className={styles.leftUpPart}>
                            <div className={styles.CurrencyTitle}>{currencyCode}</div>
                            <div className={styles.CurrencyIcon} dangerouslySetInnerHTML={{ __html: IconUp }}>
                            </div>
                        </div>
                        <div className={styles.price}>{cashRate1}<span>₽</span></div>
                    </div>

                    <div className={styles.cardPriceRight}>
                        <div className={styles.rightUpPart}>
                            <div className={styles.CurrencyTitle}>{currencyCode}</div>
                            <div className={styles.CurrencyIcon} dangerouslySetInnerHTML={{ __html: IconDown }}>
                            </div>
                        </div>
                        <div className={styles.price}>{cashRate2}<span>₽</span></div>
                    </div>
                </div>
            </div>

        </div>
    </div>
  );
};

export default CurrencyBlock;
