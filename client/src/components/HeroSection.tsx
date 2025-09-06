import './HeroSection.css';

interface HeroSectionProps {
    title: React.ReactNode;
    description: React.ReactNode;
    imageSrc: string;
}

function HeroSection(data: HeroSectionProps) {
    return (
        <div className="hero-section">
            <div className="lside-hero-sec">
                {data.title}
                {data.description}
            </div>

            <div className="rside-hero-sec">
                <img src={`/${data.imageSrc}`} className='hero-sec-img' />
            </div>
        </div>
    );
}

export default HeroSection;